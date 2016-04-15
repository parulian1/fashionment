"use strict";
String.prototype.trim = function(){
    return this.replace(/^\s*|\s*$/g,'');
}

String.prototype.ltrim = function(){
    return this.replace(/^\s*/g,'');
}

String.prototype.rtrim = function(){
    return this.replace(/\s*$/g,'');
}
String.prototype.parseIfInt = function(){
    var parsed = parseInt(this);
    return this == parsed+'' ? parsed : this.toString();
}
String.prototype.urlSplit = function(){
    var split_url = this.split('?',2);
    var url = split_url[0];

    var gets_str_list = split_url.length == 2 ? split_url[1].split('&') : [];
    var gets={}
    for(var i=0; i<gets_str_list.length; i++){
        gets_list = gets_str_list[i].split('=',2);
        if(gets_list.length == 2){
            gets[gets_list[0]] = gets_list[1].parseIfInt();
        }
    }
    return { url:url, gets:gets }
}
Array.prototype.keysToValues = function(dict){
    var values=[];
    if(dict){
        var keys = this;
        for(var i=0; i<this.length; i++){
            if(keys[i].indexOf('.') > -1){
                //if keys[j] contains eg. 'model.brand'
                //must split it to 2 arrays
                var splitted_keys = keys[i].split('.');
                var build_dict = dict;
                for( var j=0; j<splitted_keys.length; j++){
                    //using typeof instead of just build_dict[] so 0 is accepted
                    build_dict = typeof(build_dict[splitted_keys[j]]) != 'undefined' ? build_dict[splitted_keys[j]] : alert(splitted_keys[j-1]+' '+splitted_keys[j]) ;

                }
                values[i] = build_dict;
            }
            else{
                values[i] = dict[keys[i]];
            }
        }
    }
    return values;
}
/*
Array.prototype.evalKeysToValues = function(dict){
    var values=[];
    if(dict){
        var keys = this;
        for(var i=0; i<this.length; i++){
            values[i] = dict[keys[i]];
        }
    }
    return values;
}
*/

$.fn.extend({
    reverse : [].reverse,
    get_anchor:function(custom_anchor){
        // Find anchor element by finding the parent just before 'body'
        // this is to make sure that the cover is aligned even if the div is centered with margin:auto and static width
        var anchor = null
        if(custom_anchor && typeof(custom_anchor)=='object' && 'jquery' in custom_anchor){
            anchor = custom_anchor
        }
        else if(false){
            // use first child of body as anchor
            // DISABLED
            var parents= $(this).parents()
            var body_index = parents.index($('body'))
            var body_first_child = parents.eq(body_index-1)
            anchor = body_first_child
        }
        else{
            anchor = this.parent()
        }
        anchor.css('position','relative')
        return anchor
    },
    get_dimension_position_based_on:function(anchor){
        var width = this.outerWidth();
        var height = this.outerHeight();
        var top  = this.offset().top - parseInt(anchor.offset().top)
        var left  = this.offset().left - parseInt(anchor.offset().left)
        return {
            'top':top,
            'left':left,
            'width':width,
            'height':height
        }
    },
    cover:function(){
        var color=false, opacity=false, tag='div', anchor={}
        if(arguments.length == 1 && typeof(arguments[0]) == 'object'){
            var options = arguments[0]
            color = options.color
            opacity = options.opacity
            tag = options.tag || 'div'
            anchor = options.anchor && typeof(options.anchor) == 'object' && 'jquery' in options.anchor ? options.anchor : false
        }
        else{
            color = (arguments.length == 1 || arguments.length == 2) ? arguments[0] : false
            opacity = (arguments.length == 2) ? arguments[1] : false
        }

        // make this element's parent an anchor by default if no custom anchor specified
        anchor = this.get_anchor(anchor)

        var covers = $([]);
        this.each(function(i){
            var id = $(this).attr('id') ? $(this).attr('id')+'_cover' : '' ;

            var box = $(this).get_dimension_position_based_on(anchor)

            var width = box.width;
            var height = box.height;
            var top = box.top
            var left = box.left

            var style_str = 'width:'+width+'px;height:'+height+'px;position:absolute;top:'+top+'px;left:'+left+'px;'
            //if arguments are set then inline style for background-color and opacity will be applied
            style_str += color ? 'background-color:'+color+';' : ''
            style_str += opacity ? 'opacity:'+opacity+';' : ''

            var cover = $('<'+tag+' id="'+id+'" class="cover" style="'+style_str+'"></'+tag+'>').appendTo(anchor);
            covers = covers.add(cover);
        });
        if(covers.length){
            return covers;
        }
        else{
            return this;
        }
    },
    covers:function(){
        if(arguments.length == 1){
            // exactly 1 argument only
            // "thou shalt not 'cover' thy neighbour's ox"
            var ox = $(arguments[0])
            var width = ox.width()
            var height = ox.height()
            var top = ox.offset().top
            var left = ox.offset().left

            this.css({
                'display':'block',
                'position':'absolute',
                'width':width,
                'height':height,
                'top':top,
                'left':left
            })
        }
        else{
            return this
        }
    },
    hoverText:function(text,options0){
        var options = typeof(options0) == 'object' ? options0 : {}
        var anchor = options.anchor && typeof(options.anchor) == 'object' && 'jquery' in options.anchor ? options.anchor : false
        var id = "#"+$(this).attr('id')+"_cover"
        var focus_textbox = $(this)
        var input_box_all_category = $(this).cover({'anchor':anchor})
        if(text){
            input_box_all_category.html(text)
        }
        if($(this).val()=='')
        {
            input_box_all_category.show()
        }
        else
        {
            input_box_all_category.hide()
        }
        input_box_all_category.click(function(){
            $(this).hide()
            focus_textbox.focus()
        })
        $(this).focus(function(){
            input_box_all_category.hide()
        })
        $(this).blur(function(){
            if($(this).val()=='')
            {
                input_box_all_category.show()
            }
        })
    },
    attachBlock:function(content){
        if( this.data('use_attr') ){
            if( this.data('use_attr') == 'html' )
                this.html(content);
            else
                this.attr(this.data('user_attr'),content);
        }
        return this;
    },
    slideShow:function(settings0){
        var settings = settings0 ? settings0 : {}
        var url = settings.url ? settings.url : '';

        var split_url=url.urlSplit();
        url = split_url.url;
        var gets = split_url.gets;

        var start_index = settings.start_index ? settings.start_index : gets.start_index ? gets.start_index : 0;
        var end_index = settings.end_index ? settings.end_index : gets.end_index ? gets.end_index : 0;
        var num_indexes = settings.num_indexes ? settings.num_indexes : gets.num_indexes ? gets.num_indexes : 0;


        num_indexes = num_indexes ? num_indexes : start_index < end_index ? end_index-start_index : this.length ? this.length : 0;

        //WRAP THIS
        this.wrapAll('<div class="slide_show"><div class="container"><div class="items" style="float:left"></div></div></div>');

        var items = this;
        var items_box = items.parent();

        var items_box_width = 3; //should be 0, but doing this because of ie6
        this.each(function(i){
            items_box_width+=$(this).outerWidth(true);
        });

        var num_object_container = this.filter(':lt('+num_indexes+')');
        var container_width = 0;
        num_object_container.each(function(i){
            container_width+=$(this).outerWidth(true);
        });
        if(num_object_container.length <= 0)
            container_width = items_box_width;

        items_box.css({'position':'absolute','width':items_box_width,'left':0});

        var items_box_height = items_box.height();
        var items_box_container = items_box.parent().css({'position':'relative','float':'left','width':container_width,'height':items_box_height,'margin':'auto','overflow':'hidden'});
        var slide_show = items_box_container.parent();

        var current_width = container_width;
        var current_left = 0 ;
        var leftest = current_left ;
        var rightest = current_left ;
        var current_index = start_index;

        var left_arrow = $('<a href="#" class="left_arrow" style="float:left;display:block"></a>').prependTo(slide_show).click(function(e){
            e.preventDefault();

            if(current_left < rightest){
                $(this).css('cursor','pointer').attr('class','left_arrow');
                right_arrow.css('cursor','pointer').attr('class','right_arrow');
                current_left += container_width;
                items_box.animate({'left':current_left},300);
            }
            else{
                $(this).css('cursor','default').attr('class','no_arrow');
            }
        });

        var final_leftest=1;
        var right_arrow = left_arrow.clone().attr('class','right_arrow').appendTo(slide_show).click(function(e){
            e.preventDefault();
            var this_arrow = $(this);
            var already_loaded_indexes = 0;

            if(current_left == final_leftest){
                this_arrow.css('cursor','default').attr('class','no_arrow');
            }
            else if(current_left == leftest){
                current_width += container_width;
                current_left -= container_width;
                leftest = current_left;
                current_index += num_indexes;

                //eg. 6 items using slideshow, only show 5 num_indexes, 1 is already loaded
                already_loaded_indexes = items.length > current_index ? items.length - current_index : 0;

                settings.start_index = current_index + already_loaded_indexes;
                settings.end_index = current_index + num_indexes;

                items_box.css('width',current_width);

                if(already_loaded_indexes >= num_indexes){
                    items_box.animate({'left':current_left},300);
                }
                else{
                    this_arrow.removeClass("right_arrow").attr('class','loading_arrow')
                    items.more(settings,
                        function(data){
                            //on success
                            this_arrow.removeClass("loading_arrow").attr('class','right_arrow')
                            items_box.animate({'left':current_left},300);
                            return true;
                        },
                        function(){
                            //on error
                            if(already_loaded_indexes > 0){
                                //ajax failed but there are still preloaded items to be shown, slide show continues
                                items_box.animate({'left':current_left},300);
                                final_leftest = current_left ;
                            }
                            else{
                                final_leftest = current_left + container_width;
                                current_left = final_leftest;
                                leftest = current_left;
                                current_width -= container_width;
                                current_index -= num_indexes;

                                this_arrow.css('cursor','default').attr('class','no_arrow');
                            }
                        }
                    ).appendTo(items_box);
                }
            }
            else if(current_left > leftest){
                this_arrow.css('cursor','pointer').attr('class','right_arrow');
                left_arrow.css('cursor','pointer').attr('class','left_arrow');

                current_left -= container_width;
                items_box.animate({'left':current_left},300);
            }
        })
        return slide_show;
    },
    more:function(settings0,on_success0,on_error0){
        var on_success = on_success0 ? on_success0 : false;
        var on_error = on_error0 ? on_error0 : false;
        var settings = settings0 ? settings0 : {}

        var url = settings.url ? settings.url : alert('Must fill settings.url');

        var split_url = url.urlSplit();

        url = split_url.url;
        var gets = split_url.gets;

        var start_index = settings.start_index ? settings.start_index : gets.start_index ? gets.start_index : 0;
        var end_index = settings.end_index ? settings.end_index : gets.end_index ? gets.end_index : 0;
        var num_indexes = settings.num_indexes ? settings.num_indexes : this.length ? this.length : 0;


        var anchor = $('<div class="anchor"></div>');

        if(end_index > start_index)
            num_indexes = end_index - start_index;

        else if(num_indexes >= 0)
            end_index = start_index + num_indexes;

        var first_copy=this.eq(0);
        var edit_blocks_settings = settings.edit_blocks;
        var copies = $([]);


        //var copy2 = $.extend(true,{},first_copy)

        //var copy = $.extend(true,first_copy.clone(),first_copy)
//        var copy = first_copy.clone();
        //copy.appendTo('.pic_boxes')
//        copies=copies.add(copy)

        //CONVERT SELECTOR-LIKE SETTINGS TO SETTINGS ARRAY
        var edit_blocks_settings_list = [];
        for(var j=0; j<edit_blocks_settings.length; j++){
            //find all editable blocks
            //convert argument regex to array list
            var my_regex = edit_blocks_settings[j][0];
            var interpolate_list = edit_blocks_settings[j][1];

            var split = my_regex.split('=',2);
            var first_half = split[0];
            var interpolate_str = split[1].trim();

            var split2 = first_half.split('|',2) ;
            var selector = split2[0].trim();
            var attr = split2[1].trim();

            edit_blocks_settings_list[j]={}
            edit_blocks_settings_list[j]['selector'] = selector ;
            edit_blocks_settings_list[j]['attr'] = attr ;
            edit_blocks_settings_list[j]['interpolate_str'] = interpolate_str ;
            edit_blocks_settings_list[j]['interpolate_list'] = interpolate_list ;
        }
        $.ajax({
            url:url,
            type:"get",
            //data:{'order_num': escape(nlc.order_num)},
            data:{'start_index':start_index,'end_index':end_index},
            dataType:"json",
            success:function(data0,textStatus){
                var data = data0;
                num_indexes = data.length < num_indexes ? data.length : num_indexes;
                //CREATE MULTIPLE COPIES
                for(var i=0; i<num_indexes; i++){
                    var copy = first_copy.clone();
                    var edit_blocks = $([]);
                    for(var j=0; j<edit_blocks_settings_list.length; j++){
                        var ebs_list = edit_blocks_settings_list[j];
                        //find all editable blocks in first copy

                        var selector = ebs_list['selector'];
                        var attr = ebs_list['attr'];
                        var interpolate_str = ebs_list['interpolate_str'];
                        var interpolate_list = ebs_list['interpolate_list'];

                        var data_dict ={'attr':attr,'interpolate_str':interpolate_str,'interpolate_list':interpolate_list}

                        var edit_block = copy.find(selector);
                        var edit_block_data = edit_block.data('settings');
                        if(edit_block_data){
                            edit_block_data[edit_block_data.length] = data_dict;
                        }
                        else{
                            edit_block.data('settings',[data_dict]);
                        }
                        edit_blocks = edit_blocks.add(edit_block) ;
                    }
                    copy.data('edit_blocks',edit_blocks);
                    copies = copies.add(copy);
                }

                //CREATE FUNCTION TO FILL ALL EDIT_BLOCKS IN ALL COPIES
                copies.extend({
                    fillEditBlocks:function(json_list){
                        this.each(function(i){ //each copy
                            var dict = json_list[i];
                            $(this).data('edit_blocks').each(function(j){ //each edit block
                                var block = $(this);
                                var settings = $(this).data('settings');

                                for(var i=0; i< settings.length; i++){
                                    var attr = settings[i].attr;
                                    var interpolate_str = settings[i].interpolate_str;
                                    var interpolate_list = settings[i].interpolate_list.keysToValues(dict);
                                    var content = interpolate(interpolate_str,interpolate_list);
                                    if(attr == 'html')
                                        block.html(content);
                                    else
                                        block.attr(attr,content);
                                }
                            })
                        });
                    }
                })
                copies.fillEditBlocks(data);
                anchor.replaceWith(copies);

                if(typeof(on_success) == 'function')
                    on_success(data);
            },
            error:function(xhr,err,e){
                anchor.remove();
                if(typeof(on_error) == 'function')
                    on_error();
            }
        })

        return anchor;
    },
    createSortBar:function(){
        if(this.length != 1){
            alert('createSortBar: Must have only 1 element');
            return 0 ;
        }
        if(this[0].tagName.toLowerCase() != 'select'){
            alert("createSortBar: Must be a 'select' element, NOT "+this[0].tagName);
            return 0 ;
        }
        var sort_bar=$('<div id="sort_bar"><span class="label">Sort by:</span></div>');
        //CREATE ALL SORT BUTTONS AND APPEND IT
        var select=this;
        var select_form=this.parents('form');
        var select_options=select.children();
        select_options.each(function(i){
          var a = $('<a>'+$(this).html()+'</a>').appendTo(sort_bar);
          if($(this).is(':selected')){
            //if sort by input is selected, make the sort button unclickable
            a.addClass('selected') ;
          }
          else{
            //form sort by input blank, make sort button clickable for form submit
            a.attr('href','#').data('query',$(this).val()).click(function(e){
              e.preventDefault();
              select.val($(this).data('query'));
              select_form.submit() ;
            });
          }
          if(i==0){
            a.addClass('first');
          }
          else if(select_options.length-1 == i){
            a.addClass('last');
          }
        })
        return sort_bar;
    },
    totalWidth:function(){
        var total_width=0;
        this.each(function(i){
           total_width+=$(this).width();
        });
        return total_width;
    },
    totalHeight:function(){
        var total_height=0;
        this.each(function(i){
           total_height+=$(this).height();
        });
        return total_height;
    },
    reset:function(){
      $(this).find('input[type=text],select').val('');
    },
    submitLoad:function(){
      var form = $(this);
      var submit_buttons=$(this).find('input[type=submit]');
      if(submit_buttons.length < 1){
        return 0;
      }
      var submit_button = submit_buttons.eq(submit_buttons.length-1).extend({
            'reappear':function(){
                if(this.length > 0)
                    this.removeAttr('disabled').show();
            },
            'disappear':function(){
                // put outside of form so enter key or button will not be triggered while loading
                if(this.length > 0)
                    this.attr('disabled',true).hide();
            }
      });

      $(this).data('submit_button',submit_button);
      var load_image=$('<div></div>')
        .css({
          'background':"url(/media/img/preloader-small.gif) no-repeat center center",
          'width':(submit_button.width()>=79) ? submit_button.width() : 79,
          'height':(submit_button.height()>=16) ? submit_button.height() : 16,
          'cursor':'default'
        })
        .attr('class',submit_button.attr('class'))
        .hide()
        .insertAfter(submit_button);

      $(this).data('loader',load_image).submit(function(){
        submit_button.disappear();
        load_image.show();
      });
      return this;
    },
    enable:function(do_disable0){
        do_disable = do_disable0 || false
        var submit_load = $(this).data('loader') || false
        return this.each(function(i){
            var form = $(this)
            var disablee = $([])
            if($(this)[0].tagName.toLowerCase() == 'form'){
                //////////////////////
                // FIND FORM FIELDS //
                //////////////////////
                if($(this).data('fields')){
                    disablee = $(this).data('fields')

                }
                else{
                    disablee = $(this).find('input,textarea,select')
                }
                /////////////////////////
                // FIND TINYMCE FIELDS //
                /////////////////////////
                if($(this).data('tinymces')){
                    if(do_disable){
                        $(this).data('tinymces').hide();
                        $(this).data('textareas').show();
                    }
                    else{
                        $(this).data('tinymces').show();
                        $(this).data('textareas').hide();
                    }
                }
                else{
                    if(window['tinyMCE']){
                        var tinymces = $([])
                        var textareas = $([])
                        for (editor in tinyMCE.editors){
                            var textarea = $(this).find('#'+editor)
                            if(textarea.length){
                                var tinymce
                                if(do_disable){
                                    textarea.show();
                                    tinymce = $(tinyMCE.editors[editor].container).hide();
                                }
                                else{
                                    textarea.hide();
                                    tinymce = $(tinyMCE.editors[editor].container).show();
                                }
                                textareas = textareas.add(textarea)
                                tinymces = tinymces.add(tinymce)
                            }
                        }
                        $(this).data('tinymces',tinymces)
                        $(this).data('textareas',textareas)
                    }
                }
                //////////////////
                // CACHE FIELDS //
                //////////////////
                $(this).data('fields',disablee)
            }
            if(do_disable){
                // disable
                disablee.attr('disabled',true)
                // hide submit button
                if(submit_load){
                    form.find('input[type=submit]').hide()
                    //disablee.filter('input[type=submit]').show()
                    if(form.data('loader')){
                        form.data('loader').show()
                    }
                }
            }
            else{
                // enable
                disablee.removeAttr('disabled')
                if(submit_load){
                    form.find('input[type=submit]').show()
                    //disablee.filter('input[type=submit]').hide()
                    if(form.data('loader')){
                        form.data('loader').hide()
                    }
                }
            }
        });
    },
    disable:function(){
        return this.enable(true);
    },
    myAjaxForm:function(options0){
        if(!window['gettext'])
            alert("must load 'gettext' javascript")
        //INIT
        var options = options0 || {}
        var popup_when_done = options.popup_when_done || false
        var edit_again = typeof(options.edit_again) == 'undefined' ? false : typeof(options.edit_again) == 'string' && options.edit_again ? options.edit_again : 'Edit Again'
        var add_another = typeof(options.add_another) == 'undefined' ? false : typeof(options.add_another) == 'string' && options.add_another ? options.add_another : 'Add Another'
        var done = typeof(options.done) == 'string' && options.done ? options.done : 'Done'
        var form = this

        form.submitLoad();
        form.data('fields',form.find('input,textarea,select'))
        var submit_button = form.data('submit_button')

        //TODO other means to get submit_button
        if(!submit_button)
            submit_button = form.find('input[type=submit]').eq(0)

        var cover = null
        if(popup_when_done){
            cover = form.cover().hide();
        }
        else{
            cover = $([])
        }
        done = $('<div class="done" style="display:none"><b>'+gettext(done)+'</b></div>').insertAfter(submit_button)
        var not_done = $('<span class="error" style="display:none"><b>'+gettext("Error! Sorry, try again later. Maybe submit page not returning as JSON.")+'</b> </span>').insertAfter(submit_button)

        if(edit_again){
            edit_again = $('<a class="edit_again" href="#">'+gettext(edit_again)+'</a>').appendTo(done)
        }
        if(add_another){
            add_another = $('<a class="add_another" href="#">'+gettext(add_another)+'</a>').appendTo(done)
        }

        var error_outputs = $([])
        var final_options = $.extend({},options)

        final_options.dataType = options.dataType ? options.dataType : 'json'

        //django views request.is_ajax does not work with file upload
        //so add hidden input field named 'file_ajax'
        //to enable the django view to pick up on the 'file_ajax' post request instead of is_ajax
        form.append('<input name="file_ajax" type="hidden" />')

        var reload_recaptcha = form.find('a.reload_recaptcha')

        //END INIT

        ////////////////
        // DONE CLICK //
        ////////////////
        done.click(function(e){
            e.preventDefault();
            form.enable();
            cover.hide();
            done.hide();

            if(reload_recaptcha.length > 0){
                reload_recaptcha.triggerHandler('click')
            }
        });

        ///////////////////////
        // ADD ANOTHER CLICK //
        ///////////////////////
        if(add_another){
            add_another.show().click(function(e){
                done.triggerHandler('click')

                //reset form
                form[0].reset();

                //reset tinyMCE editors
                for(var i in tinyMCE.editors){
                    if(form.find('#'+i).length > 0){
                        tinyMCE.editors[i].load();
                    }
                }

                //focus first field
                var first_field = form.data('fields').eq(0)

                if($.scrollTo){
                    $.scrollTo(first_field.offset().top-40,200,function(){

                        first_field.focus();
                    });
                }
                else{
                    first_field.focus();
                }
            });
        }

        ////////////////////////////////////
        // BEFORE SUBMIT | ON SUBMIT CLICK//
        ////////////////////////////////////
        if(window['tinyMCE']){
            // tinyMCE exists
            // makes sure that the textarea is updated by tinymce before data is serialized and submitted by form
            // http://maestric.com/doc/javascript/tinymce_jquery_ajax_form
            $('form').bind('form-pre-serialize', function(e) {
                tinyMCE.triggerSave();
            });
        }

        final_options.beforeSubmit = function(data0,form0,options0){
            form.disable();
            done.hide();
            not_done.hide();
            error_outputs.remove() //remove the error elements
            error_outputs=$([]) //blanks the error_outputs variable
            if(options.beforeSubmit)
                options.beforeSubmit(data0,form0,options0)
        }

        ////////////////
        // ON SUCCESS //
        ////////////////
        final_options.success = function(data,status){
            form.data('loader') && form.data('loader').hide()
            if(typeof data != "object")
                alert('data is not a JSON object')

            var field_errors = data.errors || data.field_errors || false
            var data_success = data.status == 'success' || ('success' in data && data.success) || false

            if(data_success){
                // SUCCESS - SUCCESS
                cover.show();
                done.show().find('a').eq(0).focus();
            }
            else if(field_errors && typeof(field_errors) == 'object'){
                // SUCCESS - ERROR
                form.enable()
                if(reload_recaptcha.length > 0){
                    // reload recatpcha image
                    reload_recaptcha.triggerHandler('click')
                }
                Array.prototype.createErrorElement = function(){
                    var errors_str = ''
                    for(var i=0;i<this.length;i++){
                         errors_str += ' '+this[i]
                    }
                    var error_output = $('<span class="errors">'+errors_str+'</span>')
                    return error_output ;
                }
                form.data('fields').each(function(i){
                    var name = $(this).attr('name')
                    if(name in field_errors){
                        var error_output = field_errors[name].createErrorElement();
                        $(this).after(error_output);
                        error_outputs = error_outputs.add(error_output);
                    }
                });
                if('__all__' in field_errors){ //__all__ is non field errors
                    var error_output = field_errors['__all__'].createErrorElement();
                    form.prepend(error_output)
                    error_outputs = error_outputs.add(error_output)
                }

                var first_error = error_outputs.eq(0)
                if($.scrollTo){
                    //#scrollTo first field with error
                    $.scrollTo(first_error.offset().top-10,200,function(){
                        // prev is the field
                        first_error.prev().focus();
                    });
                }
                else{
                    //focus first field with error
                    // prev is the field
                    first_error.prev().focus();
                }
            } //end field error

            if(options.success)
                options.success(data,status)

            // after custom success
            if(form.parent().length<=0){
                // form is no longer in DOM
                // so hide the cover, since the cover is meant to cover the form
                cover.hide()
            }
        }
        //////////////
        // ON ERROR //
        //////////////
        final_options.error= function(data,status){
            form.enable()
            if(reload_recaptcha.length > 0){
                // reload recaptcha
                reload_recaptcha.triggerHandler('click')
            }
            //not_done.show();
            if(options.error)
                options.error(data,status)
        }
        form.ajaxForm(final_options)

        //LAST INIT
        if(popup_when_done){
            //centered last so that all content are filled first to get actual size to get proper center
            form.center(done).css('z-index',1)
        }
    },
    center:function(el,options0){
        var options = typeof(options0) == 'object' ? options0 : {}
        var anchor = options.anchor && typeof(options.anchor) == 'object' && 'jquery' in options.anchor ? options.anchor : false

        anchor = this.get_anchor(anchor)

        var box = this.get_dimension_position_based_on(anchor)

        var absolute = $(el);

        var this_width = box.width;
        var this_height = box.height;
        var this_top = box.top
        var this_left = box.left

        var this_center_top = this_top + this_height / 2
        var this_center_left = this_left + this_width / 2

        absolute.appendTo(anchor)

        if(absolute){
            absolute.css({
                'position':'absolute',
                'left':this_center_left,
                'top':this_center_top
            })
            var width = absolute.outerWidth()
            var height = absolute.outerHeight()
            absolute.css({
                'margin-left':-width/2,
                'margin-top':-height/2
            })
            return absolute;
        }
        else if(this){
            return this;
        }
        return false;
    },
    gallery:function(){
      var gallery=this.data('last_big_image',$(this).find('.big_image div'))
      if(gallery.length<1){
        return 0;
      }
      var small_images=$(this).find('.small_images div a')
      if(small_images.length<1){
        return 0;
      }
      small_images.click(function(e){
        e.preventDefault();
        gallery.data('last_big_image').css('background-image','url('+$(this).attr('href')+')')
      })
      return this
    },
    image:function(src, f){
      return this.each(function(){
        var i = new Image();
                i.src = src;
                i.onload = f;
                this.appendChild(i);
      })
    },
    ticker:function(){
        var ticker_content = this
        var speed_index = arguments.length ? parseInt(arguments[0]) : 2

        ticker_content.css('white-space','nowrap') //must do css white-space nowrap first! to get height then apply relative and absolute properties
        var height = ticker_content.height();

        ticker_content
        .wrapAll('<div id="'+this.attr('id')+'_wrapper" style="position:relative;overflow:hidden;height:'+height+'px;"></div>') //determine true width after twrapped with position relative
        .css({'position':'absolute','top':0});

        var width = ticker_content.width();
        var parent_width = ticker_content.parent().width();
        if(width < parent_width)
            // content is too short to need ticker animation
            return this;

        var time = parseInt(width/parent_width) * 15000 * speed_index
        var seconds = 0
        var counter
        var start_up = true
        function doTimer(){
            seconds+=1000
        }
        counter = setInterval(doTimer,1000)

        function animate_loop(){
            seconds = 0
            ticker_content.css('left',parent_width)
            ticker_content.animate({'left':-width},time,'linear',animate_loop)
        }
        animate_loop()

        var already_hovering = true
        $.fn.extend({
            'resume':function(){
                if( ! already_hovering){
                    counter = setInterval(doTimer,1000)
                    already_hovering = true
                    return $(this).animate({'left':-width},time-seconds,'linear',animate_loop)
                }
            },
            'pause':function(){
                if(already_hovering){
                    clearInterval(counter)
                    already_hovering = false
                    return $(this).stop();
                }
            }
        })
        // HOVER or FOCUS to pause/resume ticker
        ticker_content.hover(
            $.fn.pause,
            $.fn.resume
        )
        // #NOTE: DIFFERENCE BETWEEN MOUSEOVER/MOUSEOUT AND MOUSEENTER/MOUSELEAVE
        // 'div' has child 'a'
        // 'div' has event mouseover and mouseout
        // if mouse goes over 'a', it would trigger 'div' mouseout event
        // and if mouse goes out 'a', it would trigger 'div' mouseover event
        // MOUSEENTER/LEAVE DOES NOT DO THIS
        // if mouseenter/leave is used instead, mouse overing/outing 'a' will not trigger 'div' mouseover/out events
        $(document).bind('mouseenter',function(e){
            ticker_content.resume()
        })
        $(document).bind('mouseleave',function(e){
            ticker_content.pause()
        })
        // CLICK on ticker to stop it completely
        // TODO not working
        /*
        var toggle=true;
        ticker_content.click(
            function(e){
                this_ticker_content=$(this)
                if(toggle){
                    $(this).unbind('mouseout');
                    $(document).unbind('focus')
                }
                else{
                    $(this).bind('mouseout',$.fn.resume);
                    $(document).bind('focus',function(){ticker_content.resume()})
                }
                toggle=!toggle;
            }
        )
        */
        return this
    },
    groups:function(sub_group0){
        var group=this;
        var sub_group=$(sub_group0).hide();
        var init_fail = false

        if ( group.length <= 0){
            error_msg = 'Group not found' ;
            init_fail = true
        }
        else if ( group.length > 1 ){
            error_msg = 'ONLY 1 group can adopt a sub_group' ;
            init_fail = true
        }

        if ( sub_group.length <= 0 ){
            error_msg = 'Sub Group not found';
            init_fail = true
        }
        else if ( sub_group.length > 1 ){
            error_msg = 'group can adopt ONLY 1 sub_group';
            init_fail = true
        }

        var group_options = group.find('option')
        var sub_group_options = sub_group.find('option')

        if ( group_options.length <= 0 ){
            error_msg =  'Group has no options' ;
            init_fail = true
        }

        if ( sub_group_options.length <= 0 ){
            error_msg = 'Sub Group has no options';
            init_fail = true
        }

        if(init_fail){
            group.show()
            alert(error_msg)
            return 0
        }

        sub_group.data('options',sub_group_options);
        sub_group.data('group',group);

        var sub_group_copy = sub_group.clone().empty().show()
            .data('last_options',$([]))
            .attr({'id':sub_group.attr('id')+'_copy','name':sub_group.attr('name')+'_copy'})
            .data('sub_group',sub_group)
            .insertAfter(sub_group)
            .change(function(e){
                e.preventDefault();
                sub_group.val($(this).val());
            })
            .extend({
                update:function(){
                    var sub_group = $(this).data('sub_group')
                    var group = sub_group.data('group')

                    $(this).data('last_options').remove();
                    if(sub_group.data('group').val()){
                        var last_options = sub_group
                            .find('option[name='+group.val()+']')
                            .clone()
                            .appendTo($(this));

                            $(this).val(sub_group.val());

                        $(this).data('last_options',last_options)
                    }
                }
            })

        //Have copy accessible and updatable through sub_group
        sub_group.data('copy',sub_group_copy).extend({
            update:function(){
                $(this).data('copy').update();
            }
        })

        if(!sub_group.data('options').eq(0).val()){
            //if there is an empty option, append to clone
            sub_group_copy.append('<option>'+sub_group.data('options').eq(0).html()+'</option>')
        }

        if(group.data('copy')){
            //copy of group used if chaining more than 2 select boxes, since group is hidden so change event cannot pick up
            group_or_copy = group.data('copy')
        }
        else{
            group_or_copy = group
        }

        group_or_copy.change(function(e){
            sub_group_copy.update();
            sub_group_copy.triggerHandler('change');
        })

        //on load
        if ( sub_group.val() && group.val() != sub_group.find(':selected').attr('name')){
            //if sub_group has a value
            //TRAVERSE and select group related to sub_group

            //FIND GROUP'S GROUP THROUGH RECURRENCE
            var traverse_groups = []
            var traverse_sub_group = sub_group
            var traverse_i = 0

            while(traverse_sub_group.data('group')){
                //traverse groups collects the sub/groups (eg. region) that need updating later
                traverse_groups[traverse_i] = traverse_sub_group

                //group (eg. city) that needs to equal the sub group's (eg. region) name
                var current_group = traverse_groups[traverse_i].data('group').val(traverse_groups[traverse_i].find(':selected').attr('name'))
                //set this group (eg. city) as sub group for next loop
                traverse_sub_group = current_group
                traverse_i++
            }
            for(var i=traverse_groups.length-1; i>=0; i--){
                //get all previously collected 'traverse groups' and update them
                traverse_groups[i].data('copy').update();
            }
        }
        else if ( group.val() ){
            //group has a value
            //so sub group should update itself
           sub_group.update()
        }
        return sub_group;
    },
    transferOptions:function(select,is_selected){
        var children= is_selected ? this.find(':selected') : this.children();
        /*
        var children=this.children()
        if(is_selected) children.filter(':selected')
        */
        children.removeAttr('selected').appendTo(select)
        return this;
    },
    transferSelectedOptions:function(select){
        return this.transferOptions(select,'is_selected');
    },
    transferAllOptions:function(select){
        return this.transferOptions(select);
    },
    splitMultiSelect:function(settings0){
        var settings = settings0 ? settings0 : {}
        var instant_select = settings.instant_select ? settings.instant_select : true;
        var pretty = settings.pretty ? settings.pretty : false;

        var sub_group_copy = this.data('copy');
        var sub_group = this;

        if(sub_group_copy && sub_group_copy.attr('multiple')){
            var selector = $('<div class="selector"><div class="selector-available"></div></div>');
            sub_group_copy.wrap(selector).unbind('change');

            var selector_available = sub_group_copy.parent();

            var selector_chosen = $('<div class="selector-chosen"></div>').insertAfter(selector_available)
            var select_str = pretty ? '<div></div>' : '<select multiple="multiple"></select>'
            var sub_group_copy_chosen = $(select_str).appendTo(selector_chosen).data('sub_group',sub_group).extend({
                update:function(){
                    var options_values=[]
                    this.children().each(function(i){
                       options_values[i]=$(this).val()
                    })
                    this.data('sub_group').val(options_values)
                    /* ABOVE METHOD IS FASTER THAN THIS
                    sub_group_copy_chosen.children().attr('selected','selected')
                    sub_group.val(sub_group_copy_chosen.val())
                    sub_group_copy_chosen.val('')
                    */
                }
            })

            sub_group.data('chosen',sub_group_copy_chosen).extend({
                update:function(){
                    this.data('chosen').update();
                }
            })

            var choose_all = $('<a href="#" class="selector-chooseall">Choose All</a>').appendTo(selector_available).click(function(e){
                e.preventDefault();
                //sub_group_copy.transferAllOptions(sub_group_copy_chosen)
                sub_group_copy_chosen.reverseAllOptions(sub_group_copy);
                sub_group.update();
            })

            var clear_all = $('<a href="#" class="selector-clearall">Clear All</a>').appendTo(selector_chosen).click(function(e){
                e.preventDefault();
               //sub_group_copy_chosen.children().attr('selected','selected')
               sub_group_copy_chosen.transferAllOptions(sub_group_copy);
               sub_group.update();
            })

            /************* SELECTOR CHOOSER *************/
            var selector_chooser=$('<ul class="selector-chooser"></ul>').insertAfter(selector_available).css({
                'float':'left'
            })
            var li = $('<li></li>').appendTo(selector_chooser)
            var add_button=$('<a href="#" class="selector-add"></a>').appendTo(li).click(function(e){
                e.preventDefault();
                sub_group_copy.transferSelectedOptions(sub_group_copy_chosen);
                sub_group.update();

            })
            var li2 = $('<li></li>').appendTo(selector_chooser)
            var remove_button=$('<a href="#" class="selector-remove"></a>').appendTo(li2).click(function(e){
                e.preventDefault();
                sub_group_copy_chosen.transferSelectedOptions(sub_group_copy);
                sub_group.update();
            })
            /* end SELECT CHOOSER */

            add_button.triggerHandler('click')

            if(instant_select){
                selector_chooser.hide();
                $('<div class="selector-2way" style="float:left"></div>').insertAfter(selector_chooser);

                sub_group_copy.change(function(e){
                    e.preventDefault();
                    add_button.triggerHandler('click')
                })
                sub_group_copy_chosen.change(function(e){
                    e.preventDefault();
                    remove_button.triggerHandler('click')
                })
            }
        }
        return selector;
    },
    toSelect:function(list){
      return this.each(function(i){
          var input=$(this)
          if (input[0].tagName.toLowerCase() != 'input'){
              alert('toSelect: tags must be <input>')
              return input ;
          }
          var select=$('<select></select>').attr('id',input.attr('id')+'_copy').insertAfter(input).change(function(e){
              input.val($(this).val())
          })
          var options = ''
          for(var j=0;j<list.length;j++){
              options += '<option value="'+list[j][0]+'">'+list[j][1]+'</option>'
          }
          select.html(options)
          String.prototype.isInt=function(){
            return this == parseInt(this);
          }
          String.prototype.roundTo=function(list0){
              var list=list0
              var val=this
              if( !this.isInt() ){
                  return val ;
              }

              var ascending=true

              if( list[0][0] && list.length >= 2 && list[0][0] > list[1][0] ){
                ascending=false
              }
              else if( list.length >= 3 && list[1][0] > list[2][0] ){
                ascending=false
              }
              for(var i=0;i<list.length;i++){
                  var diff1 = 0
                  var diff2 = 0
                  if( ascending ){
                      //option is in ascending order, lowest to largest options
                          if( val < list[i][0] ){
                             diff1 = val - list[i-1][0]
                             diff2 = list[i][0] - val
                             val =( diff1 < diff2 ) ? list[i-1][0]: list[i][0]
                             break
                          }
                  }
                  else{
                      //option is in descending order, largest to lowest options
                          if( list[i][0] && val > list[i][0] ){
                             diff1 = list[i-1][0] - val
                             diff2 = val - list[i][0]
                             val =( diff1 < diff2 ) ? list[i-1][0]: list[i][0]
                             break
                          }
                  }
              }
              return val;
          }
          function showSelect(e){
              $(this).html('Edit');
              var  input_val=input.val();
              select.val(input_val);
              if( !select.val() && input_val.isInt() ){
                  //select does not have an option equalling the input value,
                  //BUT
                  //input is a proper number so continue to create select box
                  input_val=input_val.roundTo(list);
                  select.val(input_val);
              }
              select.show();
              input.hide();
          }
          function showInput(e){
              $(this).html('V')
              if(input.is(':hidden')){
                  //prevents input from equalling select val on first load
                  input.show().val(select.val())
              }
              select.hide();
          }
          select.val(input.val())
          if( select.val() || (!select.val() && !input.val())){
              //select has an option equalling the input value
              //OR
              //select and input are empty, so first load will have select box anyway
              firstFunction=showSelect
              secondFunction=showInput
          }
          else{
              firstFunction=showInput
              secondFunction=showSelect
          }
          var toggler=$('<a href="#" class="toggle_input_select_button" style="position:absolute;top:0;left:5px"></a>').appendTo($('<span style="position:relative"></span>').insertAfter(select))
            .toggle(firstFunction,secondFunction);

          toggler.triggerHandler('click')
          return select;
      })
    },
    tabulate:function(){
        var tabs_container=$('<div class="tabulate"></div>')
        var last_selected=$([])
        var links = ''
        var inputs = []
        var selected_index = -1

        this.each(function(i){
            inputs[i]=$(this)
            if($(this).is(':checked'))
                selected_index = i
            //avoiding 'append' inside a loop

                if ($(this)[0].tagName == 'OPTION')
                    {
                    links += '<a class="tab'+$(this).val()+'" href=""><span></span></a>'
                    }
                else{
                    links += '<a class="tab'+$(this).val()+'" href=""><span>'+this.nextSibling.textContent+'</span></a>'
                }

        })
        tabs_container.html(links).children().each(function(i){
            $(this).data('input',inputs[i]).click(function(e){
                e.preventDefault();
                if ($(this).data('input')[0].tagName == 'OPTION')
                    {$(this).data('input').attr('selected',true)}
                else{
                   $(this).data('input').attr('checked',true)}

                last_selected.removeClass('selected')
                $(this).addClass('selected')
                last_selected=$(this)
            })
            if( selected_index == i )
                $(this).triggerHandler('click')
        })
        return tabs_container;
    },
    mailhide:function(url,dict){
        var on_load = dict && typeof(dict.load) == 'function' ? dict.load : function(){}
        var do_success = dict && typeof(dict.success) == 'function' ? dict.success : function(){}
        var td = $(this)
        $.ajax({
            type:'GET',
            url:url,
            success: function(html){
                td.html(html);
                var form = td.find('form')


                // do success here before myAjaxForm,
                // so you can add custom submit button before myAjaxForm
                on_load(html)

                // focus input
                form.find('input').eq(0).focus()

                form.myAjaxForm({
                    type:'POST',
                    dataType:'json',
                    url:url,
                    success: function(data){
                        if(data['success']==true){
                            td.html(data['erase_string'])

                            if($.effects){
                                // requires jquery-ui effects.core.js for below to work
                                td.css({'background':'#f4c31d'}).animate({'backgroundColor':'#fff'},1000)
                            }
                            do_success(html)
                        }
                    }
                });
            }
        });
    },
    hotdeal_package:function(){
        var a=0 //initial to ajax
        $(this).click(function(e){
            var target =$(e.target)
            e.preventDefault()
            var href=target.attr('href')

            var add_hotdeal_form = target.parents('form').css('position','relative')

            var item_row = target.parent().parent()
            var item_id =item_row.attr('id')
            var mask= item_row.cover()
            var item_title = item_row.find('.item_data a').clone()
            var item_checkbox = item_row.find('input').clone()
            var window_content = $("<span>Choose your Hotdeal :</span>")
            var hotdeal_content = $('<div class="hotdeal_content" style="margin-bottom:6px;"></div>')
            var hotdeal_cancel = $(" <a href='#'class='close yellow_button' style='color:white;padding:2px;'> Cancel </a>")
            $('#'+ item_id +'_cover').addClass('class_cover')
            $('.class_cover').css({'opacity':'0.5','filter':'alpha(opacity=50);','background':'white'})
            item_checkbox.attr('checked',true)
            if(a==0)//initial call ajax
            {
            var win = $('<div id="win_hotdeal"></div>').appendTo('body')
            item_checkbox.appendTo(hotdeal_content)
            item_title.appendTo(hotdeal_content)
            win.html('<div class="ajax_hotdeal" style="background:#F4C31D none repeat scroll 0 0;padding:20px;border:1px black solid;"><div>')
            $('.ajax_hotdeal').parent().css({'z-index':100})
            $.ajax({
                    type:'GET',
                    url:href,
                    success: function(data){
                        var ajax_hotdeal = win.children().html(data)

                        hotdeal_content.prependTo(ajax_hotdeal.find('form'))
                        window_content.prependTo(ajax_hotdeal)
                        hotdeal_cancel.appendTo(ajax_hotdeal.find('form'))

                           ajax_hotdeal.find('form').myAjaxForm({
                                type:'POST',
                                dataType: 'json',
                                success: function(data){
                                        for(i=0;i<data.length; i++){
                                            var item = $('input[value='+data[i]+']')
                                            item.parent().parent().find('.choose_hotdeal').replaceWith('<a class="green_button">Featuring On Hot Deals</a>')
                                            win.remove();
                                            $('.class_cover').remove();
                                            a=0
                                        }
                                }

                            })

                       $('.close').click(function(e){
                            e.preventDefault()
                            win.remove();
                            $('.class_cover').remove();
                            a=0
                        })


                    }
                })

            add_hotdeal_form.center(win)
            a+=1

            }
            else{//use current ajax
                item_checkbox.appendTo(hotdeal_content)
                item_title.appendTo(hotdeal_content)
                hotdeal_content.prependTo($('#add_hotdeal_form'))

            }

        })
    },
    mptt:function(dict0){
        var dict = dict0||{}
        var pattern = dict.pattern || '---'
        var modifiers = "g"
        var tag = dict.tag || "div"
        var box_tag = (tag == "ul" || tag == "ol" ) ? tag : "div"
        var box_child_tag = (box_tag == "ul" || box_tag == "ol ") ?  "li" : tag || "div"
        var value_attr = "rel"
        var indent=new RegExp(pattern,modifiers);
        var last_indent = 0
        var select_html=''
        var match_length_count = 0
        var select_box = this
        var already_selected_options = []
        var keep_open = $.isArray(dict.keep_open) ? dict.keep_open : []

        //determine if keep_open array contains integers or strings, but not mixed
        //by seeing what data type is in the first index
        var integer_value = typeof(keep_open[0]) == 'number' ? true : false;

        var keep_open_indexes = []
        var open_lvl = dict.open_lvl || 0
        var first_match_count = 0
        var show_ancestors=false
        var shown_ancestors=false

        var options = select_box.find('option')
        var options_last_index = options.length-1
        options.reverse().each(function(i){
            var value = integer_value ? parseInt($(this).val()) : $(this).val()
            var match_length = $(this).html().match(indent)
            if(i==0){
                //GET FIRST OPTION
                //if first option has indent
                //then all with that amount of indent is counted as first child
                //which could have 'li' tag
                first_match_count = match_length ? match_length.length :0
            }
            if(match_length){
                //at least one match
                var match_length_count = match_length.length
            }
            else{
                match_length_count=0
            }
            var num_close_tags= last_indent - match_length_count

            //test if tag should be a li or div
            var tag = match_length_count > first_match_count ? 'div' : box_child_tag
            var style = match_length_count <= open_lvl ? '' : ' style="display:none"'
            if(last_indent > match_length_count){
                if(last_indent>1){
                    $(this).append('(<span>+</span>)')
                }

            }
            if($(this).is(':selected')){
                show_ancestors=true
                shown_ancestors=true
            }
            if(show_ancestors && num_close_tags > -1){
                style=''
            }
            else{
                show_ancestors=false
            }
            var open_tag = '<'+tag+' '+value_attr+'="'+i+'" class="lvl'+match_length_count+'"'+style+'>'
            var close_tag = '</'+tag+'>'
            if(num_close_tags<=0 && i){
                for(var j=0;j<Math.abs(num_close_tags)+1;j++){
                   select_html = close_tag+select_html
               }
            }
            last_indent = match_length_count
            select_html = open_tag + $(this).html().replace(indent, "")+select_html

            //GET ALL SELECTED OPTIONS ON LOAD
            if($(this).is(':selected')){
                already_selected_options[already_selected_options.length] = i;
            }

            if($.inArray(value,keep_open) > -1){
                keep_open_indexes[keep_open_indexes.length] = i;
                /*
                */
            }
        })
        // FILL MPTT BOX WITH CREATED SELECT DIVS FROM ABOVE
        var mptt_box = $('<'+box_tag+' class="mptt_box"></'+box_tag+'>').insertAfter(select_box).html(select_html);
        //LAST LOOP
        //IF OPTION IS ALREADY SELECTED, ITS ANCESTORS ARE SHOWN
        //SO
        //SHOW ROOT DIV AND ITS CHILDREN
        if(shown_ancestors){
            mptt_box.children().show();
            mptt_box.children().children().show();
        }

        var last_select = $([])
        var last_toggle = 0
        var box = $(".mptt_box").click(function(e,tgt){
            e.preventDefault();
            var target = $(tgt || e.target)
            //target_value MUST BE INTEGER even if integer_value is true //maybe I meant false
            var target_value = parseInt(target.attr(value_attr))
            var values = {}
            if(target.is("["+value_attr+"]")){

                var option_index = target.attr(value_attr)
                //if(last_select.length > 0 && last_select.attr('['+value_attr+']') == target.attr('['+value_attr+']')){
                if( ! target.is('.selected')){
                    //currently not selected so:
                    //SELECT this and UNSELECT its ancestors
                    //below

                    //UNSELECT its ancestor
                    var closest = target.closest(".selected,.mptt_box");
                    var closest_option_index = closest.attr(value_attr);

                    if(closest.is('.selected') && closest.attr(value_attr) != target.attr(value_attr)){
                        //found ancestor
                        //so REMOVE SELECTION FROM ANCESTOR
                        closest.removeClass("selected");
                        options.eq(closest_option_index).removeAttr('selected');
                    }
                    if( $.inArray(target_value,keep_open_indexes) <= -1){
                        //SHOW CHILDREN if target is not meant to be kept opened
                        target.children().show();
                        last_toggle =1
                        target.find('span:first').html('-')
                    }
                    //SELECT this
                    target.addClass("selected")
                    options.eq(option_index).attr('selected','selected')
                    if( ! select_box.attr('multiple')){
                        last_select.removeClass("selected")
                        //last_select.children().hide();
                        last_select = target;
                    }
                }
                else{
                    //currently selected
                    //so do unselection
                    if(select_box.attr('multiple')){
                        //MULTIPLE SELECT BOX behaviour
                        //so UNSELECT this
                        target.removeClass("selected");
                        options.eq(option_index).removeAttr('selected');

                        if( $.inArray(target_value,keep_open_indexes) <= -1){
                            //UNSELECT and HIDE its CHILDREN if this is not meant to be kept opened
                                target.find(tag).hide()
                        }
                    }
                    else{
                        //SINGLE SELECT BOX behaviour
                        if( $.inArray(target_value,keep_open_indexes) <= -1){
                            //UNSELECT and TOGGLE its CHILDREN if this is not meant to be kept opened
                            var calculate =last_toggle % 2
                            if(calculate==1){
                                target.find('span:first').html('+')
                            }
                            else{
                                target.find('span:first').html('-')
                            }

                            if(target.data('children_toggle')){
                                target.data('children_toggle').toggle()
                            }
                            else{
                                var children_toggle = target.find(tag)
                                children_toggle.toggle()
                                target.data('children_toggle',children_toggle)
                            }
                            last_toggle+=1
                        }
                    }
                }
                //must UNSELECT this descendants whether this is currently SELECTED or UNSELECTED
                var selected_children = target.find(".selected").each(function(i){
                    $(this).removeClass('selected');
                    options.eq($(this).attr('rel')).removeAttr('selected');
                })
            }
        })
        //SELECT THE DIVS WHICH OPTIONS ARE ALREADY SELECTED ON LOAD
        //may not need this if select options are looped reverse above
        $.each(already_selected_options,function(i){
            box.find('[rel='+this+']').click().show()
            .siblings().show();
        })
        $.each(keep_open_indexes,function(i){
            box.find('[rel='+this+']').children().show();
        })
            //already_selected_options[i]

        //box.find('option:selected').click()

        //CHANGING SELECTBOX CHANGES MPTT BOX
        select_box.change(function(e){
            var selected_options=$(this).find('option')
            box.find('['+value_attr+']').removeClass('selected')

            $(this).find('option:selected').each(function(i){
                var index=selected_options.index(this)
                var target = box.find('div[rel='+index+']')
                target.addClass('selected')
                target.siblings().show()
            })
            //selected_option_indexes[i]=select_box.index(this)
        })

        return box;
    },
    popupform:function(dict){
        if(dict){
            this_form=$(this)
            var window_content=''
            var warning = dict.row.warning
            var window_content_header = warning+" : <ul>"
            var window = this_form.data('window')
            var win = $([])
            if (window && window.length){
                win = window
                window.show()
            }else{
                win = $('<div class="pop_up_window"></div>')
                .appendTo('body')
                this_form.data('window',win)
            }
            var checked_inputs = $(dict.row.input)
            if (window && window.length){
                // POP UP WINDOW ALREADY CREATED
                checked_inputs.each(function()
                {
                    var tag_name = $(this)[0].tagName.toLowerCase()
                    if (tag_name == 'input'){
                        var tag = '<input type="'+$(this).attr('type')+'" value="'+$(this).val()+'"'
                        if ($(this).attr('type') == 'checkbox' || $(this).attr('type') == 'radio'){
                            tag+='checked="checked"'
                        }
                        tag+=' />'
                    }
                    window_content = window_content + "<li>"+tag+$(this).parents(dict.row.attr).find(dict.row.title).html() + "<a id='remove_selected_item' href=''>remove</a></li>";

                });
            }
            else{
                // CREATE POP UP WINDOW
                window_content = window_content_header
                checked_inputs.each(function()
                {
                    var tag_name = $(this)[0].tagName.toLowerCase()
                    if (tag_name == 'input'){
                        var tag = '<input name="'+$(this).attr('name')+'" type="'+$(this).attr('type')+'" value="'+$(this).val()+'"'
                        if ($(this).attr('type') == 'checkbox' || $(this).attr('type') == 'radio'){
                            tag+='checked="checked"'
                        }
                        tag+=' />'
                    }
                    window_content = window_content + "<li>"+tag+$(this).parents(dict.row.attr).find(dict.row.title).html() + "<a id='remove_selected_item' href=''>remove</a></li>";

                });
                if(!checked_inputs.length){
                    window_content = "Please select products you want to Delete <a href='#' class='confirm red_button'> Ok </a> "
                }
                else{
                    window_content = window_content + "</ul>"+ "<input type='submit' class='confirm red_button' value='Yes'></input>" + " <a href='#'class='close yellow_button'> Cancel </a>"
                }
            }

            if (window && window.length){
                // pop up window already created
                this_form.data('window').find('ul').html(window_content)
            }else{
                // create pop up window
                var copy_form_id = this_form.attr('id') ? this_form.attr('id')+'_copy' : '';
                this_form.data('window').html('<form id="'+copy_form_id+'" class="copy_form" method="'+this_form.attr('method')+'" action="'+this_form.attr('action')+'"><div>'+window_content+'</div></form>')
            }

            checked_inputs.each(function(i){
                if ($(this).data('cover') && $(this).data('cover').length){
                    $(this).data('cover').show()
                }
                else{
                    $(this).data('cover',$(this).parents(dict.row.attr).cover())
                }
                $(this).data('cover').center(this_form.data('window')).fadeIn(600);
            })
            //this_form
            //this_form

            win.find('a:#remove_selected_item').each(function(i){
                $(this).click(function(h){
                    h.preventDefault()
                    checked_inputs.eq(i).removeAttr('checked')
                    if ($(this).parents('ul').children().length==1){
                        $('.close').click()
                    }
                    $(this).parent().remove()
                    //$('#'+checked_inputs.eq(i).attr('value')+'_cover').hide()
                    checked_inputs.eq(i).data('cover').hide()
                })
            })

//            $('.confirm').click(function(e){
//                e.preventDefault()
//                if(checked_inputs.length){
//                    win.find('form').submit()
//                }
//                win.hide();
//            })

            $('.close').click(function(e){
                e.preventDefault()
                checked_inputs.each(function(i){
                    $(this).data('cover').hide()
                })
                win.hide();
            })
        }
    }
})
function ajaxLoginSignup(){
        if(arguments.length < 2){
            return 0;
        }
        login_str = arguments[0];
        signup_str = arguments[1];
        options = arguments[2] || {};

        on_login_load = options && typeof(options.on_login_load) == 'function' ? options.on_login_load : function(){}
        on_sign_up_load = options && typeof(options.on_sign_up_load) == 'function' ? options.on_sign_up_load : function(){}
        on_close = options && typeof(options.on_close) == 'function' ? options.on_close : function(){}

        /*
            options are:
                'closeable': true/false
                'on_login_load': function
                'on_sign_up_load': function
        */

        var id_login = $(login_str);
        var id_sign_up = $(signup_str);

        // AJAX HOLDER MUST COME AFTER COVER
        // so that its z-index comes in front of cover
        // TODO maybe below does not need to append to body first??
        var ajax_holder = $('<div id="ajax_holder" class="form_box"></div>').appendTo('body');

        if(options.closeable){
            // CLOSE LOGIN/SIGN UP BUTTON
            // &
            // DON'T SHOW LOGIN/SIGN UP AGAIN BUTTON
            var close_holder = $('<div style="float:right"><a href="" id="dont_show_again">Do not show this again</a>&nbsp;<a href="" class="close_ajax"></a></div>').appendTo(ajax_holder)
            var close_ajax = close_holder.find('.close_ajax').click(function(e){
                e.preventDefault()
                ajax_holder.hide()
                on_close()
            })
            var dont_show_again = $('#dont_show_again').click(function(e){
                e.preventDefault()
                close_ajax.triggerHandler('click')
                $.cookie('no_login_popup', true, { expires: 0.5 })
            })
            // end close login sign up don't show again button
        }

        id_sign_up.click(function(e){
            e.preventDefault()
            ajax_holder.find('.ajax_form_holder').hide()
            var link = $(this).attr('href')
            var this_sign_up_box = $(this)

            if(this_sign_up_box.data('ajax_remember'))
            {
                this_sign_up_box.data('ajax_remember').show()
            }
            else{
                $.ajax({
                    type:'GET',
                    dataType:'html',
                    url:link,
                    success: function(html){
                        var ajax_sign_up_holder = $('<div class="ajax_form_holder"></div>').appendTo(ajax_holder)
                        ajax_sign_up_holder.html('<h1>'+gettext('Sign Up')+'</h1><form action="'+link+'" method="POST">'+html+'<div class="last_row"><input type="submit" class="submit_button" value="'+gettext('Sign Up')+'"></div></form>')

                        //LOGIN BUTTON NEXT TO SUBMIT BUTTON
                        $('<a href="#" class="login link">'+gettext('Login')+'</a>').insertAfter(ajax_sign_up_holder.find('.submit_button')).click(function(e){
                          e.preventDefault()
                          id_login.triggerHandler('click')
                        })
                        var signup_form = ajax_sign_up_holder.find('form:eq(0)')
                        this_sign_up_box.data('ajax_remember',ajax_sign_up_holder)
                        signup_form.myAjaxForm({
                            success: function(data){
                                if (data.status=="success"){
                                    var user = data.user || False
                                    ajax_sign_up_holder.hide()
                                    if(options.closeable)
                                        dont_show_again.hide()
                                    ajax_holder.append('<div class="submit_success">'+gettext('Thank you for signing up.<br />You are now logged in.')+'</div>')
                                    ajax_holder.click(function(e){
                                        e.preventDefault()
                                        if(options.closeable)
                                            close_ajax.triggerHandler('click')
                                    })
                                    if(user){
                                        $('#login_signup_button_container').html('Welcome '+user.first_name+' '+user.last_name+' <a href="/accounts/edit/">Edit</a>'+'<a href="/accounts/logout/" class="blue_button">Logout</a>')
                                    }
                                }
                            }
                        })
                        on_sign_up_load(ajax_holder)
                    }
                })
            }
            $.cookie("pop_sign_up_first",1)
        })
        id_login.click(function(e){
            var link = $(this).attr('href')
            e.preventDefault()
            ajax_holder.find('.ajax_form_holder').hide()
            var this_login_box = $(this)
            if(this_login_box.data('ajax_remember_login'))
            {
                this_login_box.data('ajax_remember_login').show()
            }
            else{
                $.ajax({
                  type:'GET',
                  dataType:'html',
                  url:link,
                  success: function(html){
                      var ajax_login_holder = $('<div class="ajax_form_holder"></div>').appendTo(ajax_holder)
                      ajax_login_holder.html('<h1>'+gettext('Login')+'</h1><form action="'+link+'" method="POST">'+html+'<div class="last_row"><input type="submit" class="submit_button" value="'+gettext('Login')+'"></div></form>')

                      //SIGN UP BUTTON NEXT TO SUBMIT BUTTON
                        $('<a href="#" class="sign_up link">'+gettext('Sign Up')+'</a>').insertAfter(ajax_login_holder.find('.submit_button')).click(function(e){
                          e.preventDefault()
                          id_sign_up.triggerHandler('click')
                        })

                      var login_form = ajax_login_holder.find('form:eq(0)')
                      this_login_box.data('ajax_remember_login',ajax_login_holder)
                      login_form.myAjaxForm({
                          success: function(data){
                              if (data.status=="success"){
                                  var user = data.user || False
                                  ajax_login_holder.hide()
                                  if(options.closeable)
                                      dont_show_again.hide()
                                  ajax_holder.append('<div class="submit_success">'+gettext('You are now logged in.')+'</div>')

                                  ajax_holder.click(function(e){
                                      e.preventDefault()
                                      if(options.closeable)
                                          close_ajax.triggerHandler('click')
                                  })
                                  /*
                                  if(user){
                                      $('#login_signup_button_container').html('Welcome '+user.first_name+' '+user.last_name+' <a href="/accounts/edit/">Edit</a>'+'<a href="/accounts/logout/" class="blue_button">Logout</a>')
                                  }
                                  */
                              }
                          }
                      })
                      on_login_load(ajax_holder)
                  }
              })
          }
          $.cookie("pop_sign_up_first",null)
        })
        if( $.cookie && ! $.cookie("no_login_popup") ){
            if( $.cookie("pop_sign_up_first") ){
                id_sign_up.triggerHandler('click')
            }
            else{
                id_login.triggerHandler('click')
            }
        }
        return ajax_holder
}
jQuery.each({
    centerOf: 'center',
    groupBy: 'groups',
    reverseAllOptions:'transferAllOptions'
}, function(name, original){
    jQuery.fn[ name ] = function() {
        var args = arguments;

        return this.each(function(){
            for ( var i = 0, length = args.length; i < length; i++ )
                jQuery( args[ i ] )[ original ]( this );
        });
    }
});
function MultiFormWizard(dict){
    //load and show loader first
    var loader=$('<div id="wizard_loader"></div>').css({'background-image':'url(/media/img/preloader.gif)'}).hide().insertBefore(dict.forms[0])
    var forms_with_error=false
    for(var i=0;i<dict.forms.length;i++){
        //hide forms first
        dict.forms[i].hide();

        var last_form=dict.forms[i].filter(':last')
        var current_forms=dict.forms[i]
        var next_forms=dict.forms[(i+1)%dict.forms.length]
        var previous_forms=dict.forms[(i-1)%dict.forms.length]

        var next_previous_button=$('<a href="#"></a>')
          .data('current_forms',current_forms)
          .data('next_previous_forms',next_forms)
          .appendTo(last_form)
          .click(function(e){
            e.preventDefault();
            //$(this).data('current_forms').hide();
            //$(this).data('next_previous_forms').show();
                var first_step=$(this).data('current_forms').hide();
                var last_step=$(this).data('next_previous_forms').hide();
                loader.show().css('height',first_step.totalHeight()).animate({
          //        'background':'#fff'
                  'height':last_step.totalHeight()
                },200,function(){
                  $(this).hide(); //this=loader
                  last_step.show()
                });
          });


        if( (i+1) == dict.forms.length){
            //add real submit button to last form
            dict.form.find('input[type=submit]').appendTo(last_form);
        }
        else{
          var next_button=$.extend({},next_previous_button)
            .html(gettext('Next'));

          var next_button_class = (dict.next_button_class) ? dict.next_button_class : 'next'
          next_button.addClass(next_button_class)
        }
        var error_class=( dict.error_class ) ? dict.error_class  :'errors'
        if(!forms_with_error && dict.forms[i].find('.'+error_class).length>0){
            //forms with latest error except first form
            //error or not, first form will show anyway
            forms_with_error=dict.forms[i]
        }
        if(i>0){
          //all step have back button except first
          var back_button=$.extend({},next_previous_button)
            .data('next_previous_forms',previous_forms)
            .css({'color':"#1B7DF0",'float':'left','margin-right':5})
            .html(gettext('Back'));

          var back_button_class = (dict.back_button_class) ? dict.back_button_class : 'back'
          back_button.addClass(back_button_class)
        }
        //hide all steps first
        dict.forms[i].hide();
    } //end loop all forms/step
    if(forms_with_error){
        //form with error found
        forms_with_error.show();
    }
    else{
        //or just show the first form
        dict.forms[0].show()
    }
}

Paginator =
{
    jumpToPage: function(pages,getvars)
    {
        var page = prompt(interpolate(gettext("Enter a number between 1 and %s to jump to that page"),[pages]), "");
        if (page != undefined)
        {
            page = parseInt(page, 10)
            if (!isNaN(page) && page > 0 && page <= pages)
            {
                window.location.href = "?page=" + page + getvars;
            }
        }
    }
}
