"use strict";String.prototype.trim=function(){return this.replace(/^\s*|\s*$/g,'');}
String.prototype.ltrim=function(){return this.replace(/^\s*/g,'');}
String.prototype.rtrim=function(){return this.replace(/\s*$/g,'');}
String.prototype.parseIfInt=function(){var parsed=parseInt(this);return this==parsed+''?parsed:this.toString();}
String.prototype.urlSplit=function(){var split_url=this.split('?',2);var url=split_url[0];var gets_str_list=split_url.length==2?split_url[1].split('&'):[];var gets={}
for(var i=0;i<gets_str_list.length;i++){gets_list=gets_str_list[i].split('=',2);if(gets_list.length==2){gets[gets_list[0]]=gets_list[1].parseIfInt();}}
return{url:url,gets:gets}}
Array.prototype.keysToValues=function(dict){var values=[];if(dict){var keys=this;for(var i=0;i<this.length;i++){if(keys[i].indexOf('.')>-1){var splitted_keys=keys[i].split('.');var build_dict=dict;for(var j=0;j<splitted_keys.length;j++){build_dict=typeof(build_dict[splitted_keys[j]])!='undefined'?build_dict[splitted_keys[j]]:alert(splitted_keys[j-1]+' '+splitted_keys[j]);}
values[i]=build_dict;}
else{values[i]=dict[keys[i]];}}}
return values;}
$.fn.extend({reverse:[].reverse,get_anchor:function(custom_anchor){var anchor=null
if(custom_anchor&&typeof(custom_anchor)=='object'&&'jquery'in custom_anchor){anchor=custom_anchor}
else if(false){var parents=$(this).parents()
var body_index=parents.index($('body'))
var body_first_child=parents.eq(body_index-1)
anchor=body_first_child}
else{anchor=this.parent()}
anchor.css('position','relative')
return anchor},get_dimension_position_based_on:function(anchor){var width=this.outerWidth();var height=this.outerHeight();var top=this.offset().top-parseInt(anchor.offset().top)
var left=this.offset().left-parseInt(anchor.offset().left)
return{'top':top,'left':left,'width':width,'height':height}},cover:function(){var color=false,opacity=false,tag='div',anchor={}
if(arguments.length==1&&typeof(arguments[0])=='object'){var options=arguments[0]
color=options.color
opacity=options.opacity
tag=options.tag||'div'
anchor=options.anchor&&typeof(options.anchor)=='object'&&'jquery'in options.anchor?options.anchor:false}
else{color=(arguments.length==1||arguments.length==2)?arguments[0]:false
opacity=(arguments.length==2)?arguments[1]:false}
anchor=this.get_anchor(anchor)
var covers=$([]);this.each(function(i){var id=$(this).attr('id')?$(this).attr('id')+'_cover':'';var box=$(this).get_dimension_position_based_on(anchor)
var width=box.width;var height=box.height;var top=box.top
var left=box.left
var style_str='width:'+width+'px;height:'+height+'px;position:absolute;top:'+top+'px;left:'+left+'px;'
style_str+=color?'background-color:'+color+';':''
style_str+=opacity?'opacity:'+opacity+';':''
var cover=$('<'+tag+' id="'+id+'" class="cover" style="'+style_str+'"></'+tag+'>').appendTo(anchor);covers=covers.add(cover);});if(covers.length){return covers;}
else{return this;}},covers:function(){if(arguments.length==1){var ox=$(arguments[0])
var width=ox.width()
var height=ox.height()
var top=ox.offset().top
var left=ox.offset().left
this.css({'display':'block','position':'absolute','width':width,'height':height,'top':top,'left':left})}
else{return this}},hoverText:function(text,options0){var options=typeof(options0)=='object'?options0:{}
var anchor=options.anchor&&typeof(options.anchor)=='object'&&'jquery'in options.anchor?options.anchor:false
var id="#"+$(this).attr('id')+"_cover"
var focus_textbox=$(this)
var input_box_all_category=$(this).cover({'anchor':anchor})
if(text){input_box_all_category.html(text)}
if($(this).val()=='')
{input_box_all_category.show()}
else
{input_box_all_category.hide()}
input_box_all_category.click(function(){$(this).hide()
focus_textbox.focus()})
$(this).focus(function(){input_box_all_category.hide()})
$(this).blur(function(){if($(this).val()=='')
{input_box_all_category.show()}})},attachBlock:function(content){if(this.data('use_attr')){if(this.data('use_attr')=='html')
this.html(content);else
this.attr(this.data('user_attr'),content);}
return this;},slideShow:function(settings0){var settings=settings0?settings0:{}
var url=settings.url?settings.url:'';var split_url=url.urlSplit();url=split_url.url;var gets=split_url.gets;var start_index=settings.start_index?settings.start_index:gets.start_index?gets.start_index:0;var end_index=settings.end_index?settings.end_index:gets.end_index?gets.end_index:0;var num_indexes=settings.num_indexes?settings.num_indexes:gets.num_indexes?gets.num_indexes:0;num_indexes=num_indexes?num_indexes:start_index<end_index?end_index-start_index:this.length?this.length:0;this.wrapAll('<div class="slide_show"><div class="container"><div class="items" style="float:left"></div></div></div>');var items=this;var items_box=items.parent();var items_box_width=3;this.each(function(i){items_box_width+=$(this).outerWidth(true);});var num_object_container=this.filter(':lt('+num_indexes+')');var container_width=0;num_object_container.each(function(i){container_width+=$(this).outerWidth(true);});if(num_object_container.length<=0)
container_width=items_box_width;items_box.css({'position':'absolute','width':items_box_width,'left':0});var items_box_height=items_box.height();var items_box_container=items_box.parent().css({'position':'relative','float':'left','width':container_width,'height':items_box_height,'margin':'auto','overflow':'hidden'});var slide_show=items_box_container.parent();var current_width=container_width;var current_left=0;var leftest=current_left;var rightest=current_left;var current_index=start_index;var left_arrow=$('<a href="#" class="left_arrow" style="float:left;display:block"></a>').prependTo(slide_show).click(function(e){e.preventDefault();if(current_left<rightest){$(this).css('cursor','pointer').attr('class','left_arrow');right_arrow.css('cursor','pointer').attr('class','right_arrow');current_left+=container_width;items_box.animate({'left':current_left},300);}
else{$(this).css('cursor','default').attr('class','no_arrow');}});var final_leftest=1;var right_arrow=left_arrow.clone().attr('class','right_arrow').appendTo(slide_show).click(function(e){e.preventDefault();var this_arrow=$(this);var already_loaded_indexes=0;if(current_left==final_leftest){this_arrow.css('cursor','default').attr('class','no_arrow');}
else if(current_left==leftest){current_width+=container_width;current_left-=container_width;leftest=current_left;current_index+=num_indexes;already_loaded_indexes=items.length>current_index?items.length-current_index:0;settings.start_index=current_index+already_loaded_indexes;settings.end_index=current_index+num_indexes;items_box.css('width',current_width);if(already_loaded_indexes>=num_indexes){items_box.animate({'left':current_left},300);}
else{this_arrow.removeClass("right_arrow").attr('class','loading_arrow')
items.more(settings,function(data){this_arrow.removeClass("loading_arrow").attr('class','right_arrow')
items_box.animate({'left':current_left},300);return true;},function(){if(already_loaded_indexes>0){items_box.animate({'left':current_left},300);final_leftest=current_left;}
else{final_leftest=current_left+container_width;current_left=final_leftest;leftest=current_left;current_width-=container_width;current_index-=num_indexes;this_arrow.css('cursor','default').attr('class','no_arrow');}}).appendTo(items_box);}}
else if(current_left>leftest){this_arrow.css('cursor','pointer').attr('class','right_arrow');left_arrow.css('cursor','pointer').attr('class','left_arrow');current_left-=container_width;items_box.animate({'left':current_left},300);}})
return slide_show;},more:function(settings0,on_success0,on_error0){var on_success=on_success0?on_success0:false;var on_error=on_error0?on_error0:false;var settings=settings0?settings0:{}
var url=settings.url?settings.url:alert('Must fill settings.url');var split_url=url.urlSplit();url=split_url.url;var gets=split_url.gets;var start_index=settings.start_index?settings.start_index:gets.start_index?gets.start_index:0;var end_index=settings.end_index?settings.end_index:gets.end_index?gets.end_index:0;var num_indexes=settings.num_indexes?settings.num_indexes:this.length?this.length:0;var anchor=$('<div class="anchor"></div>');if(end_index>start_index)
num_indexes=end_index-start_index;else if(num_indexes>=0)
end_index=start_index+num_indexes;var first_copy=this.eq(0);var edit_blocks_settings=settings.edit_blocks;var copies=$([]);var edit_blocks_settings_list=[];for(var j=0;j<edit_blocks_settings.length;j++){var my_regex=edit_blocks_settings[j][0];var interpolate_list=edit_blocks_settings[j][1];var split=my_regex.split('=',2);var first_half=split[0];var interpolate_str=split[1].trim();var split2=first_half.split('|',2);var selector=split2[0].trim();var attr=split2[1].trim();edit_blocks_settings_list[j]={}
edit_blocks_settings_list[j]['selector']=selector;edit_blocks_settings_list[j]['attr']=attr;edit_blocks_settings_list[j]['interpolate_str']=interpolate_str;edit_blocks_settings_list[j]['interpolate_list']=interpolate_list;}
$.ajax({url:url,type:"get",data:{'start_index':start_index,'end_index':end_index},dataType:"json",success:function(data0,textStatus){var data=data0;num_indexes=data.length<num_indexes?data.length:num_indexes;for(var i=0;i<num_indexes;i++){var copy=first_copy.clone();var edit_blocks=$([]);for(var j=0;j<edit_blocks_settings_list.length;j++){var ebs_list=edit_blocks_settings_list[j];var selector=ebs_list['selector'];var attr=ebs_list['attr'];var interpolate_str=ebs_list['interpolate_str'];var interpolate_list=ebs_list['interpolate_list'];var data_dict={'attr':attr,'interpolate_str':interpolate_str,'interpolate_list':interpolate_list}
var edit_block=copy.find(selector);var edit_block_data=edit_block.data('settings');if(edit_block_data){edit_block_data[edit_block_data.length]=data_dict;}
else{edit_block.data('settings',[data_dict]);}
edit_blocks=edit_blocks.add(edit_block);}
copy.data('edit_blocks',edit_blocks);copies=copies.add(copy);}
copies.extend({fillEditBlocks:function(json_list){this.each(function(i){var dict=json_list[i];$(this).data('edit_blocks').each(function(j){var block=$(this);var settings=$(this).data('settings');for(var i=0;i<settings.length;i++){var attr=settings[i].attr;var interpolate_str=settings[i].interpolate_str;var interpolate_list=settings[i].interpolate_list.keysToValues(dict);var content=interpolate(interpolate_str,interpolate_list);if(attr=='html')
block.html(content);else
block.attr(attr,content);}})});}})
copies.fillEditBlocks(data);anchor.replaceWith(copies);if(typeof(on_success)=='function')
on_success(data);},error:function(xhr,err,e){anchor.remove();if(typeof(on_error)=='function')
on_error();}})
return anchor;},createSortBar:function(){if(this.length!=1){alert('createSortBar: Must have only 1 element');return 0;}
if(this[0].tagName.toLowerCase()!='select'){alert("createSortBar: Must be a 'select' element, NOT "+this[0].tagName);return 0;}
var sort_bar=$('<div id="sort_bar"><span class="label">Sort by:</span></div>');var select=this;var select_form=this.parents('form');var select_options=select.children();select_options.each(function(i){var a=$('<a>'+$(this).html()+'</a>').appendTo(sort_bar);if($(this).is(':selected')){a.addClass('selected');}
else{a.attr('href','#').data('query',$(this).val()).click(function(e){e.preventDefault();select.val($(this).data('query'));select_form.submit();});}
if(i==0){a.addClass('first');}
else if(select_options.length-1==i){a.addClass('last');}})
return sort_bar;},totalWidth:function(){var total_width=0;this.each(function(i){total_width+=$(this).width();});return total_width;},totalHeight:function(){var total_height=0;this.each(function(i){total_height+=$(this).height();});return total_height;},reset:function(){$(this).find('input[type=text],select').val('');},submitLoad:function(){var form=$(this);var submit_buttons=$(this).find('input[type=submit]');if(submit_buttons.length<1){return 0;}
var submit_button=submit_buttons.eq(submit_buttons.length-1).extend({'reappear':function(){if(this.length>0)
this.removeAttr('disabled').show();},'disappear':function(){if(this.length>0)
this.attr('disabled',true).hide();}});$(this).data('submit_button',submit_button);var load_image=$('<div></div>').css({'background':"url(/media/img/preloader-small.gif) no-repeat center center",'width':(submit_button.width()>=79)?submit_button.width():79,'height':(submit_button.height()>=16)?submit_button.height():16,'cursor':'default'}).attr('class',submit_button.attr('class')).hide().insertAfter(submit_button);$(this).data('loader',load_image).submit(function(){submit_button.disappear();load_image.show();});return this;},enable:function(do_disable0){do_disable=do_disable0||false
var submit_load=$(this).data('loader')||false
return this.each(function(i){var form=$(this)
var disablee=$([])
if($(this)[0].tagName.toLowerCase()=='form'){if($(this).data('fields')){disablee=$(this).data('fields')}
else{disablee=$(this).find('input,textarea,select')}
if($(this).data('tinymces')){if(do_disable){$(this).data('tinymces').hide();$(this).data('textareas').show();}
else{$(this).data('tinymces').show();$(this).data('textareas').hide();}}
else{if(window['tinyMCE']){var tinymces=$([])
var textareas=$([])
for(editor in tinyMCE.editors){var textarea=$(this).find('#'+editor)
if(textarea.length){var tinymce
if(do_disable){textarea.show();tinymce=$(tinyMCE.editors[editor].container).hide();}
else{textarea.hide();tinymce=$(tinyMCE.editors[editor].container).show();}
textareas=textareas.add(textarea)
tinymces=tinymces.add(tinymce)}}
$(this).data('tinymces',tinymces)
$(this).data('textareas',textareas)}}
$(this).data('fields',disablee)}
if(do_disable){disablee.attr('disabled',true)
if(submit_load){form.find('input[type=submit]').hide()
if(form.data('loader')){form.data('loader').show()}}}
else{disablee.removeAttr('disabled')
if(submit_load){form.find('input[type=submit]').show()
if(form.data('loader')){form.data('loader').hide()}}}});},disable:function(){return this.enable(true);},myAjaxForm:function(options0){if(!window['gettext'])
alert("must load 'gettext' javascript")
var options=options0||{}
var popup_when_done=options.popup_when_done||false
var edit_again=typeof(options.edit_again)=='undefined'?false:typeof(options.edit_again)=='string'&&options.edit_again?options.edit_again:'Edit Again'
var add_another=typeof(options.add_another)=='undefined'?false:typeof(options.add_another)=='string'&&options.add_another?options.add_another:'Add Another'
var done=typeof(options.done)=='string'&&options.done?options.done:'Done'
var form=this
form.submitLoad();form.data('fields',form.find('input,textarea,select'))
var submit_button=form.data('submit_button')
if(!submit_button)
submit_button=form.find('input[type=submit]').eq(0)
var cover=null
if(popup_when_done){cover=form.cover().hide();}
else{cover=$([])}
done=$('<div class="done" style="display:none"><b>'+gettext(done)+'</b></div>').insertAfter(submit_button)
var not_done=$('<span class="error" style="display:none"><b>'+gettext("Error! Sorry, try again later. Maybe submit page not returning as JSON.")+'</b> </span>').insertAfter(submit_button)
if(edit_again){edit_again=$('<a class="edit_again" href="#">'+gettext(edit_again)+'</a>').appendTo(done)}
if(add_another){add_another=$('<a class="add_another" href="#">'+gettext(add_another)+'</a>').appendTo(done)}
var error_outputs=$([])
var final_options=$.extend({},options)
final_options.dataType=options.dataType?options.dataType:'json'
form.append('<input name="file_ajax" type="hidden" />')
var reload_recaptcha=form.find('a.reload_recaptcha')
done.click(function(e){e.preventDefault();form.enable();cover.hide();done.hide();if(reload_recaptcha.length>0){reload_recaptcha.triggerHandler('click')}});if(add_another){add_another.show().click(function(e){done.triggerHandler('click')
form[0].reset();for(var i in tinyMCE.editors){if(form.find('#'+i).length>0){tinyMCE.editors[i].load();}}
var first_field=form.data('fields').eq(0)
if($.scrollTo){$.scrollTo(first_field.offset().top-40,200,function(){first_field.focus();});}
else{first_field.focus();}});}
if(window['tinyMCE']){$('form').bind('form-pre-serialize',function(e){tinyMCE.triggerSave();});}
final_options.beforeSubmit=function(data0,form0,options0){form.disable();done.hide();not_done.hide();error_outputs.remove()
error_outputs=$([])
if(options.beforeSubmit)
options.beforeSubmit(data0,form0,options0)}
final_options.success=function(data,status){form.data('loader')&&form.data('loader').hide()
if(typeof data!="object")
alert('data is not a JSON object')
var field_errors=data.errors||data.field_errors||false
var data_success=data.status=='success'||('success'in data&&data.success)||false
if(data_success){cover.show();done.show().find('a').eq(0).focus();}
else if(field_errors&&typeof(field_errors)=='object'){form.enable()
if(reload_recaptcha.length>0){reload_recaptcha.triggerHandler('click')}
Array.prototype.createErrorElement=function(){var errors_str=''
for(var i=0;i<this.length;i++){errors_str+=' '+this[i]}
var error_output=$('<span class="errors">'+errors_str+'</span>')
return error_output;}
form.data('fields').each(function(i){var name=$(this).attr('name')
if(name in field_errors){var error_output=field_errors[name].createErrorElement();$(this).after(error_output);error_outputs=error_outputs.add(error_output);}});if('__all__'in field_errors){var error_output=field_errors['__all__'].createErrorElement();form.prepend(error_output)
error_outputs=error_outputs.add(error_output)}
var first_error=error_outputs.eq(0)
if($.scrollTo){$.scrollTo(first_error.offset().top-10,200,function(){first_error.prev().focus();});}
else{first_error.prev().focus();}}
if(options.success)
options.success(data,status)
if(form.parent().length<=0){cover.hide()}}
final_options.error=function(data,status){form.enable()
if(reload_recaptcha.length>0){reload_recaptcha.triggerHandler('click')}
if(options.error)
options.error(data,status)}
form.ajaxForm(final_options)
if(popup_when_done){form.center(done).css('z-index',1)}},center:function(el,options0){var options=typeof(options0)=='object'?options0:{}
var anchor=options.anchor&&typeof(options.anchor)=='object'&&'jquery'in options.anchor?options.anchor:false
anchor=this.get_anchor(anchor)
var box=this.get_dimension_position_based_on(anchor)
var absolute=$(el);var this_width=box.width;var this_height=box.height;var this_top=box.top
var this_left=box.left
var this_center_top=this_top+this_height/2
var this_center_left=this_left+this_width/2
absolute.appendTo(anchor)
if(absolute){absolute.css({'position':'absolute','left':this_center_left,'top':this_center_top})
var width=absolute.outerWidth()
var height=absolute.outerHeight()
absolute.css({'margin-left':-width/2,'margin-top':-height/2})
return absolute;}
else if(this){return this;}
return false;},gallery:function(){var gallery=this.data('last_big_image',$(this).find('.big_image div'))
if(gallery.length<1){return 0;}
var small_images=$(this).find('.small_images div a')
if(small_images.length<1){return 0;}
small_images.click(function(e){e.preventDefault();gallery.data('last_big_image').css('background-image','url('+$(this).attr('href')+')')})
return this},image:function(src,f){return this.each(function(){var i=new Image();i.src=src;i.onload=f;this.appendChild(i);})},ticker:function(){var ticker_content=this
var speed_index=arguments.length?parseInt(arguments[0]):2
ticker_content.css('white-space','nowrap')
var height=ticker_content.height();ticker_content.wrapAll('<div id="'+this.attr('id')+'_wrapper" style="position:relative;overflow:hidden;height:'+height+'px;"></div>').css({'position':'absolute','top':0});var width=ticker_content.width();var parent_width=ticker_content.parent().width();if(width<parent_width)
return this;var time=parseInt(width/parent_width)*15000*speed_index
var seconds=0
var counter
var start_up=true
function doTimer(){seconds+=1000}
counter=setInterval(doTimer,1000)
function animate_loop(){seconds=0
ticker_content.css('left',parent_width)
ticker_content.animate({'left':-width},time,'linear',animate_loop)}
animate_loop()
var already_hovering=true
$.fn.extend({'resume':function(){if(!already_hovering){counter=setInterval(doTimer,1000)
already_hovering=true
return $(this).animate({'left':-width},time-seconds,'linear',animate_loop)}},'pause':function(){if(already_hovering){clearInterval(counter)
already_hovering=false
return $(this).stop();}}})
ticker_content.hover($.fn.pause,$.fn.resume)
$(document).bind('mouseenter',function(e){ticker_content.resume()})
$(document).bind('mouseleave',function(e){ticker_content.pause()})
return this},groups:function(sub_group0){var group=this;var sub_group=$(sub_group0).hide();var init_fail=false
if(group.length<=0){error_msg='Group not found';init_fail=true}
else if(group.length>1){error_msg='ONLY 1 group can adopt a sub_group';init_fail=true}
if(sub_group.length<=0){error_msg='Sub Group not found';init_fail=true}
else if(sub_group.length>1){error_msg='group can adopt ONLY 1 sub_group';init_fail=true}
var group_options=group.find('option')
var sub_group_options=sub_group.find('option')
if(group_options.length<=0){error_msg='Group has no options';init_fail=true}
if(sub_group_options.length<=0){error_msg='Sub Group has no options';init_fail=true}
if(init_fail){group.show()
alert(error_msg)
return 0}
sub_group.data('options',sub_group_options);sub_group.data('group',group);var sub_group_copy=sub_group.clone().empty().show().data('last_options',$([])).attr({'id':sub_group.attr('id')+'_copy','name':sub_group.attr('name')+'_copy'}).data('sub_group',sub_group).insertAfter(sub_group).change(function(e){e.preventDefault();sub_group.val($(this).val());}).extend({update:function(){var sub_group=$(this).data('sub_group')
var group=sub_group.data('group')
$(this).data('last_options').remove();if(sub_group.data('group').val()){var last_options=sub_group.find('option[name='+group.val()+']').clone().appendTo($(this));$(this).val(sub_group.val());$(this).data('last_options',last_options)}}})
sub_group.data('copy',sub_group_copy).extend({update:function(){$(this).data('copy').update();}})
if(!sub_group.data('options').eq(0).val()){sub_group_copy.append('<option>'+sub_group.data('options').eq(0).html()+'</option>')}
if(group.data('copy')){group_or_copy=group.data('copy')}
else{group_or_copy=group}
group_or_copy.change(function(e){sub_group_copy.update();sub_group_copy.triggerHandler('change');})
if(sub_group.val()&&group.val()!=sub_group.find(':selected').attr('name')){var traverse_groups=[]
var traverse_sub_group=sub_group
var traverse_i=0
while(traverse_sub_group.data('group')){traverse_groups[traverse_i]=traverse_sub_group
var current_group=traverse_groups[traverse_i].data('group').val(traverse_groups[traverse_i].find(':selected').attr('name'))
traverse_sub_group=current_group
traverse_i++}
for(var i=traverse_groups.length-1;i>=0;i--){traverse_groups[i].data('copy').update();}}
else if(group.val()){sub_group.update()}
return sub_group;},transferOptions:function(select,is_selected){var children=is_selected?this.find(':selected'):this.children();children.removeAttr('selected').appendTo(select)
return this;},transferSelectedOptions:function(select){return this.transferOptions(select,'is_selected');},transferAllOptions:function(select){return this.transferOptions(select);},splitMultiSelect:function(settings0){var settings=settings0?settings0:{}
var instant_select=settings.instant_select?settings.instant_select:true;var pretty=settings.pretty?settings.pretty:false;var sub_group_copy=this.data('copy');var sub_group=this;if(sub_group_copy&&sub_group_copy.attr('multiple')){var selector=$('<div class="selector"><div class="selector-available"></div></div>');sub_group_copy.wrap(selector).unbind('change');var selector_available=sub_group_copy.parent();var selector_chosen=$('<div class="selector-chosen"></div>').insertAfter(selector_available)
var select_str=pretty?'<div></div>':'<select multiple="multiple"></select>'
var sub_group_copy_chosen=$(select_str).appendTo(selector_chosen).data('sub_group',sub_group).extend({update:function(){var options_values=[]
this.children().each(function(i){options_values[i]=$(this).val()})
this.data('sub_group').val(options_values)}})
sub_group.data('chosen',sub_group_copy_chosen).extend({update:function(){this.data('chosen').update();}})
var choose_all=$('<a href="#" class="selector-chooseall">Choose All</a>').appendTo(selector_available).click(function(e){e.preventDefault();sub_group_copy_chosen.reverseAllOptions(sub_group_copy);sub_group.update();})
var clear_all=$('<a href="#" class="selector-clearall">Clear All</a>').appendTo(selector_chosen).click(function(e){e.preventDefault();sub_group_copy_chosen.transferAllOptions(sub_group_copy);sub_group.update();})
var selector_chooser=$('<ul class="selector-chooser"></ul>').insertAfter(selector_available).css({'float':'left'})
var li=$('<li></li>').appendTo(selector_chooser)
var add_button=$('<a href="#" class="selector-add"></a>').appendTo(li).click(function(e){e.preventDefault();sub_group_copy.transferSelectedOptions(sub_group_copy_chosen);sub_group.update();})
var li2=$('<li></li>').appendTo(selector_chooser)
var remove_button=$('<a href="#" class="selector-remove"></a>').appendTo(li2).click(function(e){e.preventDefault();sub_group_copy_chosen.transferSelectedOptions(sub_group_copy);sub_group.update();})
add_button.triggerHandler('click')
if(instant_select){selector_chooser.hide();$('<div class="selector-2way" style="float:left"></div>').insertAfter(selector_chooser);sub_group_copy.change(function(e){e.preventDefault();add_button.triggerHandler('click')})
sub_group_copy_chosen.change(function(e){e.preventDefault();remove_button.triggerHandler('click')})}}
return selector;},toSelect:function(list){return this.each(function(i){var input=$(this)
if(input[0].tagName.toLowerCase()!='input'){alert('toSelect: tags must be <input>')
return input;}
var select=$('<select></select>').attr('id',input.attr('id')+'_copy').insertAfter(input).change(function(e){input.val($(this).val())})
var options=''
for(var j=0;j<list.length;j++){options+='<option value="'+list[j][0]+'">'+list[j][1]+'</option>'}
select.html(options)
String.prototype.isInt=function(){return this==parseInt(this);}
String.prototype.roundTo=function(list0){var list=list0
var val=this
if(!this.isInt()){return val;}
var ascending=true
if(list[0][0]&&list.length>=2&&list[0][0]>list[1][0]){ascending=false}
else if(list.length>=3&&list[1][0]>list[2][0]){ascending=false}
for(var i=0;i<list.length;i++){var diff1=0
var diff2=0
if(ascending){if(val<list[i][0]){diff1=val-list[i-1][0]
diff2=list[i][0]-val
val=(diff1<diff2)?list[i-1][0]:list[i][0]
break}}
else{if(list[i][0]&&val>list[i][0]){diff1=list[i-1][0]-val
diff2=val-list[i][0]
val=(diff1<diff2)?list[i-1][0]:list[i][0]
break}}}
return val;}
function showSelect(e){$(this).html('Edit');var input_val=input.val();select.val(input_val);if(!select.val()&&input_val.isInt()){input_val=input_val.roundTo(list);select.val(input_val);}
select.show();input.hide();}
function showInput(e){$(this).html('V')
if(input.is(':hidden')){input.show().val(select.val())}
select.hide();}
select.val(input.val())
if(select.val()||(!select.val()&&!input.val())){firstFunction=showSelect
secondFunction=showInput}
else{firstFunction=showInput
secondFunction=showSelect}
var toggler=$('<a href="#" class="toggle_input_select_button" style="position:absolute;top:0;left:5px"></a>').appendTo($('<span style="position:relative"></span>').insertAfter(select)).toggle(firstFunction,secondFunction);toggler.triggerHandler('click')
return select;})},tabulate:function(){var tabs_container=$('<div class="tabulate"></div>')
var last_selected=$([])
var links=''
var inputs=[]
var selected_index=-1
this.each(function(i){inputs[i]=$(this)
if($(this).is(':checked'))
selected_index=i
if($(this)[0].tagName=='OPTION')
{links+='<a class="tab'+$(this).val()+'" href=""><span></span></a>'}
else{links+='<a class="tab'+$(this).val()+'" href=""><span>'+this.nextSibling.textContent+'</span></a>'}})
tabs_container.html(links).children().each(function(i){$(this).data('input',inputs[i]).click(function(e){e.preventDefault();if($(this).data('input')[0].tagName=='OPTION')
{$(this).data('input').attr('selected',true)}
else{$(this).data('input').attr('checked',true)}
last_selected.removeClass('selected')
$(this).addClass('selected')
last_selected=$(this)})
if(selected_index==i)
$(this).triggerHandler('click')})
return tabs_container;},mailhide:function(url,dict){var on_load=dict&&typeof(dict.load)=='function'?dict.load:function(){}
var do_success=dict&&typeof(dict.success)=='function'?dict.success:function(){}
var td=$(this)
$.ajax({type:'GET',url:url,success:function(html){td.html(html);var form=td.find('form')
on_load(html)
form.find('input').eq(0).focus()
form.myAjaxForm({type:'POST',dataType:'json',url:url,success:function(data){if(data['success']==true){td.html(data['erase_string'])
if($.effects){td.css({'background':'#f4c31d'}).animate({'backgroundColor':'#fff'},1000)}
do_success(html)}}});}});},hotdeal_package:function(){var a=0
$(this).click(function(e){var target=$(e.target)
e.preventDefault()
var href=target.attr('href')
var add_hotdeal_form=target.parents('form').css('position','relative')
var item_row=target.parent().parent()
var item_id=item_row.attr('id')
var mask=item_row.cover()
var item_title=item_row.find('.item_data a').clone()
var item_checkbox=item_row.find('input').clone()
var window_content=$("<span>Choose your Hotdeal :</span>")
var hotdeal_content=$('<div class="hotdeal_content" style="margin-bottom:6px;"></div>')
var hotdeal_cancel=$(" <a href='#'class='close yellow_button' style='color:white;padding:2px;'> Cancel </a>")
$('#'+item_id+'_cover').addClass('class_cover')
$('.class_cover').css({'opacity':'0.5','filter':'alpha(opacity=50);','background':'white'})
item_checkbox.attr('checked',true)
if(a==0)
{var win=$('<div id="win_hotdeal"></div>').appendTo('body')
item_checkbox.appendTo(hotdeal_content)
item_title.appendTo(hotdeal_content)
win.html('<div class="ajax_hotdeal" style="background:#F4C31D none repeat scroll 0 0;padding:20px;border:1px black solid;"><div>')
$('.ajax_hotdeal').parent().css({'z-index':100})
$.ajax({type:'GET',url:href,success:function(data){var ajax_hotdeal=win.children().html(data)
hotdeal_content.prependTo(ajax_hotdeal.find('form'))
window_content.prependTo(ajax_hotdeal)
hotdeal_cancel.appendTo(ajax_hotdeal.find('form'))
ajax_hotdeal.find('form').myAjaxForm({type:'POST',dataType:'json',success:function(data){for(i=0;i<data.length;i++){var item=$('input[value='+data[i]+']')
item.parent().parent().find('.choose_hotdeal').replaceWith('<a class="green_button">Featuring On Hot Deals</a>')
win.remove();$('.class_cover').remove();a=0}}})
$('.close').click(function(e){e.preventDefault()
win.remove();$('.class_cover').remove();a=0})}})
add_hotdeal_form.center(win)
a+=1}
else{item_checkbox.appendTo(hotdeal_content)
item_title.appendTo(hotdeal_content)
hotdeal_content.prependTo($('#add_hotdeal_form'))}})},mptt:function(dict0){var dict=dict0||{}
var pattern=dict.pattern||'---'
var modifiers="g"
var tag=dict.tag||"div"
var box_tag=(tag=="ul"||tag=="ol")?tag:"div"
var box_child_tag=(box_tag=="ul"||box_tag=="ol ")?"li":tag||"div"
var value_attr="rel"
var indent=new RegExp(pattern,modifiers);var last_indent=0
var select_html=''
var match_length_count=0
var select_box=this
var already_selected_options=[]
var keep_open=$.isArray(dict.keep_open)?dict.keep_open:[]
var integer_value=typeof(keep_open[0])=='number'?true:false;var keep_open_indexes=[]
var open_lvl=dict.open_lvl||0
var first_match_count=0
var show_ancestors=false
var shown_ancestors=false
var options=select_box.find('option')
var options_last_index=options.length-1
options.reverse().each(function(i){var value=integer_value?parseInt($(this).val()):$(this).val()
var match_length=$(this).html().match(indent)
if(i==0){first_match_count=match_length?match_length.length:0}
if(match_length){var match_length_count=match_length.length}
else{match_length_count=0}
var num_close_tags=last_indent-match_length_count
var tag=match_length_count>first_match_count?'div':box_child_tag
var style=match_length_count<=open_lvl?'':' style="display:none"'
if(last_indent>match_length_count){if(last_indent>1){$(this).append('(<span>+</span>)')}}
if($(this).is(':selected')){show_ancestors=true
shown_ancestors=true}
if(show_ancestors&&num_close_tags>-1){style=''}
else{show_ancestors=false}
var open_tag='<'+tag+' '+value_attr+'="'+i+'" class="lvl'+match_length_count+'"'+style+'>'
var close_tag='</'+tag+'>'
if(num_close_tags<=0&&i){for(var j=0;j<Math.abs(num_close_tags)+1;j++){select_html=close_tag+select_html}}
last_indent=match_length_count
select_html=open_tag+$(this).html().replace(indent,"")+select_html
if($(this).is(':selected')){already_selected_options[already_selected_options.length]=i;}
if($.inArray(value,keep_open)>-1){keep_open_indexes[keep_open_indexes.length]=i;}})
var mptt_box=$('<'+box_tag+' class="mptt_box"></'+box_tag+'>').insertAfter(select_box).html(select_html);if(shown_ancestors){mptt_box.children().show();mptt_box.children().children().show();}
var last_select=$([])
var last_toggle=0
var box=$(".mptt_box").click(function(e,tgt){e.preventDefault();var target=$(tgt||e.target)
var target_value=parseInt(target.attr(value_attr))
var values={}
if(target.is("["+value_attr+"]")){var option_index=target.attr(value_attr)
if(!target.is('.selected')){var closest=target.closest(".selected,.mptt_box");var closest_option_index=closest.attr(value_attr);if(closest.is('.selected')&&closest.attr(value_attr)!=target.attr(value_attr)){closest.removeClass("selected");options.eq(closest_option_index).removeAttr('selected');}
if($.inArray(target_value,keep_open_indexes)<=-1){target.children().show();last_toggle=1
target.find('span:first').html('-')}
target.addClass("selected")
options.eq(option_index).attr('selected','selected')
if(!select_box.attr('multiple')){last_select.removeClass("selected")
last_select=target;}}
else{if(select_box.attr('multiple')){target.removeClass("selected");options.eq(option_index).removeAttr('selected');if($.inArray(target_value,keep_open_indexes)<=-1){target.find(tag).hide()}}
else{if($.inArray(target_value,keep_open_indexes)<=-1){var calculate=last_toggle%2
if(calculate==1){target.find('span:first').html('+')}
else{target.find('span:first').html('-')}
if(target.data('children_toggle')){target.data('children_toggle').toggle()}
else{var children_toggle=target.find(tag)
children_toggle.toggle()
target.data('children_toggle',children_toggle)}
last_toggle+=1}}}
var selected_children=target.find(".selected").each(function(i){$(this).removeClass('selected');options.eq($(this).attr('rel')).removeAttr('selected');})}})
$.each(already_selected_options,function(i){box.find('[rel='+this+']').click().show().siblings().show();})
$.each(keep_open_indexes,function(i){box.find('[rel='+this+']').children().show();})
select_box.change(function(e){var selected_options=$(this).find('option')
box.find('['+value_attr+']').removeClass('selected')
$(this).find('option:selected').each(function(i){var index=selected_options.index(this)
var target=box.find('div[rel='+index+']')
target.addClass('selected')
target.siblings().show()})})
return box;},popupform:function(dict){if(dict){this_form=$(this)
var window_content=''
var warning=dict.row.warning
var window_content_header=warning+" : <ul>"
var window=this_form.data('window')
var win=$([])
if(window&&window.length){win=window
window.show()}else{win=$('<div class="pop_up_window"></div>').appendTo('body')
this_form.data('window',win)}
var checked_inputs=$(dict.row.input)
if(window&&window.length){checked_inputs.each(function()
{var tag_name=$(this)[0].tagName.toLowerCase()
if(tag_name=='input'){var tag='<input type="'+$(this).attr('type')+'" value="'+$(this).val()+'"'
if($(this).attr('type')=='checkbox'||$(this).attr('type')=='radio'){tag+='checked="checked"'}
tag+=' />'}
window_content=window_content+"<li>"+tag+$(this).parents(dict.row.attr).find(dict.row.title).html()+"<a id='remove_selected_item' href=''>remove</a></li>";});}
else{window_content=window_content_header
checked_inputs.each(function()
{var tag_name=$(this)[0].tagName.toLowerCase()
if(tag_name=='input'){var tag='<input name="'+$(this).attr('name')+'" type="'+$(this).attr('type')+'" value="'+$(this).val()+'"'
if($(this).attr('type')=='checkbox'||$(this).attr('type')=='radio'){tag+='checked="checked"'}
tag+=' />'}
window_content=window_content+"<li>"+tag+$(this).parents(dict.row.attr).find(dict.row.title).html()+"<a id='remove_selected_item' href=''>remove</a></li>";});if(!checked_inputs.length){window_content="Please select products you want to Delete <a href='#' class='confirm red_button'> Ok </a> "}
else{window_content=window_content+"</ul>"+"<input type='submit' class='confirm red_button' value='Yes'></input>"+" <a href='#'class='close yellow_button'> Cancel </a>"}}
if(window&&window.length){this_form.data('window').find('ul').html(window_content)}else{var copy_form_id=this_form.attr('id')?this_form.attr('id')+'_copy':'';this_form.data('window').html('<form id="'+copy_form_id+'" class="copy_form" method="'+this_form.attr('method')+'" action="'+this_form.attr('action')+'"><div>'+window_content+'</div></form>')}
checked_inputs.each(function(i){if($(this).data('cover')&&$(this).data('cover').length){$(this).data('cover').show()}
else{$(this).data('cover',$(this).parents(dict.row.attr).cover())}
$(this).data('cover').center(this_form.data('window')).fadeIn(600);})
win.find('a:#remove_selected_item').each(function(i){$(this).click(function(h){h.preventDefault()
checked_inputs.eq(i).removeAttr('checked')
if($(this).parents('ul').children().length==1){$('.close').click()}
$(this).parent().remove()
checked_inputs.eq(i).data('cover').hide()})})
$('.close').click(function(e){e.preventDefault()
checked_inputs.each(function(i){$(this).data('cover').hide()})
win.hide();})}}})
function ajaxLoginSignup(){if(arguments.length<2){return 0;}
login_str=arguments[0];signup_str=arguments[1];options=arguments[2]||{};on_login_load=options&&typeof(options.on_login_load)=='function'?options.on_login_load:function(){}
on_sign_up_load=options&&typeof(options.on_sign_up_load)=='function'?options.on_sign_up_load:function(){}
on_close=options&&typeof(options.on_close)=='function'?options.on_close:function(){}
var id_login=$(login_str);var id_sign_up=$(signup_str);var ajax_holder=$('<div id="ajax_holder" class="form_box"></div>').appendTo('body');if(options.closeable){var close_holder=$('<div style="float:right"><a href="" id="dont_show_again">Do not show this again</a>&nbsp;<a href="" class="close_ajax"></a></div>').appendTo(ajax_holder)
var close_ajax=close_holder.find('.close_ajax').click(function(e){e.preventDefault()
ajax_holder.hide()
on_close()})
var dont_show_again=$('#dont_show_again').click(function(e){e.preventDefault()
close_ajax.triggerHandler('click')
$.cookie('no_login_popup',true,{expires:0.5})})}
id_sign_up.click(function(e){e.preventDefault()
ajax_holder.find('.ajax_form_holder').hide()
var link=$(this).attr('href')
var this_sign_up_box=$(this)
if(this_sign_up_box.data('ajax_remember'))
{this_sign_up_box.data('ajax_remember').show()}
else{$.ajax({type:'GET',dataType:'html',url:link,success:function(html){var ajax_sign_up_holder=$('<div class="ajax_form_holder"></div>').appendTo(ajax_holder)
ajax_sign_up_holder.html('<h1>'+gettext('Sign Up')+'</h1><form action="'+link+'" method="POST">'+html+'<div class="last_row"><input type="submit" class="submit_button" value="'+gettext('Sign Up')+'"></div></form>')
$('<a href="#" class="login link">'+gettext('Login')+'</a>').insertAfter(ajax_sign_up_holder.find('.submit_button')).click(function(e){e.preventDefault()
id_login.triggerHandler('click')})
var signup_form=ajax_sign_up_holder.find('form:eq(0)')
this_sign_up_box.data('ajax_remember',ajax_sign_up_holder)
signup_form.myAjaxForm({success:function(data){if(data.status=="success"){var user=data.user||False
ajax_sign_up_holder.hide()
if(options.closeable)
dont_show_again.hide()
ajax_holder.append('<div class="submit_success">'+gettext('Thank you for signing up.<br />You are now logged in.')+'</div>')
ajax_holder.click(function(e){e.preventDefault()
if(options.closeable)
close_ajax.triggerHandler('click')})
if(user){$('#login_signup_button_container').html('Welcome '+user.first_name+' '+user.last_name+' <a href="/accounts/edit/">Edit</a>'+'<a href="/accounts/logout/" class="blue_button">Logout</a>')}}}})
on_sign_up_load(ajax_holder)}})}
$.cookie("pop_sign_up_first",1)})
id_login.click(function(e){var link=$(this).attr('href')
e.preventDefault()
ajax_holder.find('.ajax_form_holder').hide()
var this_login_box=$(this)
if(this_login_box.data('ajax_remember_login'))
{this_login_box.data('ajax_remember_login').show()}
else{$.ajax({type:'GET',dataType:'html',url:link,success:function(html){var ajax_login_holder=$('<div class="ajax_form_holder"></div>').appendTo(ajax_holder)
ajax_login_holder.html('<h1>'+gettext('Login')+'</h1><form action="'+link+'" method="POST">'+html+'<div class="last_row"><input type="submit" class="submit_button" value="'+gettext('Login')+'"></div></form>')
$('<a href="#" class="sign_up link">'+gettext('Sign Up')+'</a>').insertAfter(ajax_login_holder.find('.submit_button')).click(function(e){e.preventDefault()
id_sign_up.triggerHandler('click')})
var login_form=ajax_login_holder.find('form:eq(0)')
this_login_box.data('ajax_remember_login',ajax_login_holder)
login_form.myAjaxForm({success:function(data){if(data.status=="success"){var user=data.user||False
ajax_login_holder.hide()
if(options.closeable)
dont_show_again.hide()
ajax_holder.append('<div class="submit_success">'+gettext('You are now logged in.')+'</div>')
ajax_holder.click(function(e){e.preventDefault()
if(options.closeable)
close_ajax.triggerHandler('click')})}}})
on_login_load(ajax_holder)}})}
$.cookie("pop_sign_up_first",null)})
if($.cookie&&!$.cookie("no_login_popup")){if($.cookie("pop_sign_up_first")){id_sign_up.triggerHandler('click')}
else{id_login.triggerHandler('click')}}
return ajax_holder}
jQuery.each({centerOf:'center',groupBy:'groups',reverseAllOptions:'transferAllOptions'},function(name,original){jQuery.fn[name]=function(){var args=arguments;return this.each(function(){for(var i=0,length=args.length;i<length;i++)
jQuery(args[i])[original](this);});}});function MultiFormWizard(dict){var loader=$('<div id="wizard_loader"></div>').css({'background-image':'url(/media/img/preloader.gif)'}).hide().insertBefore(dict.forms[0])
var forms_with_error=false
for(var i=0;i<dict.forms.length;i++){dict.forms[i].hide();var last_form=dict.forms[i].filter(':last')
var current_forms=dict.forms[i]
var next_forms=dict.forms[(i+1)%dict.forms.length]
var previous_forms=dict.forms[(i-1)%dict.forms.length]
var next_previous_button=$('<a href="#"></a>').data('current_forms',current_forms).data('next_previous_forms',next_forms).appendTo(last_form).click(function(e){e.preventDefault();var first_step=$(this).data('current_forms').hide();var last_step=$(this).data('next_previous_forms').hide();loader.show().css('height',first_step.totalHeight()).animate({'height':last_step.totalHeight()},200,function(){$(this).hide();last_step.show()});});if((i+1)==dict.forms.length){dict.form.find('input[type=submit]').appendTo(last_form);}
else{var next_button=$.extend({},next_previous_button).html(gettext('Next'));var next_button_class=(dict.next_button_class)?dict.next_button_class:'next'
next_button.addClass(next_button_class)}
var error_class=(dict.error_class)?dict.error_class:'errors'
if(!forms_with_error&&dict.forms[i].find('.'+error_class).length>0){forms_with_error=dict.forms[i]}
if(i>0){var back_button=$.extend({},next_previous_button).data('next_previous_forms',previous_forms).css({'color':"#1B7DF0",'float':'left','margin-right':5}).html(gettext('Back'));var back_button_class=(dict.back_button_class)?dict.back_button_class:'back'
back_button.addClass(back_button_class)}
dict.forms[i].hide();}
if(forms_with_error){forms_with_error.show();}
else{dict.forms[0].show()}}
Paginator={jumpToPage:function(pages,getvars)
{var page=prompt(interpolate(gettext("Enter a number between 1 and %s to jump to that page"),[pages]),"");if(page!=undefined)
{page=parseInt(page,10)
if(!isNaN(page)&&page>0&&page<=pages)
{window.location.href="?page="+page+getvars;}}}};(function($){$.fn.superfish=function(op){var sf=$.fn.superfish,c=sf.c,$arrow=$(['<span class="',c.arrowClass,'"> &#187;</span>'].join('')),over=function(){var $$=$(this),menu=getMenu($$);clearTimeout(menu.sfTimer);$$.showSuperfishUl().siblings().hideSuperfishUl();},out=function(){var $$=$(this),menu=getMenu($$),o=sf.op;clearTimeout(menu.sfTimer);menu.sfTimer=setTimeout(function(){o.retainPath=($.inArray($$[0],o.$path)>-1);$$.hideSuperfishUl();if(o.$path.length&&$$.parents(['li.',o.hoverClass].join('')).length<1){over.call(o.$path);}},o.delay);},getMenu=function($menu){var menu=$menu.parents(['ul.',c.menuClass,':first'].join(''))[0];sf.op=sf.o[menu.serial];return menu;},addArrow=function($a){$a.addClass(c.anchorClass).append($arrow.clone());};return this.each(function(){var s=this.serial=sf.o.length;var o=$.extend({},sf.defaults,op);o.$path=$('li.'+o.pathClass,this).slice(0,o.pathLevels).each(function(){$(this).addClass([o.hoverClass,c.bcClass].join(' ')).filter('li:has(ul)').removeClass(o.pathClass);});sf.o[s]=sf.op=o;$('li:has(ul)',this)[($.fn.hoverIntent&&!o.disableHI)?'hoverIntent':'hover'](over,out).each(function(){if(o.autoArrows)addArrow($('>a:first-child',this));}).not('.'+c.bcClass).hideSuperfishUl();var $a=$('a',this);$a.each(function(i){var $li=$a.eq(i).parents('li');$a.eq(i).focus(function(){over.call($li);}).blur(function(){out.call($li);});});o.onInit.call(this);}).each(function(){var menuClasses=[c.menuClass];if(sf.op.dropShadows&&!($.browser.msie&&$.browser.version<7))menuClasses.push(c.shadowClass);$(this).addClass(menuClasses.join(' '));});};var sf=$.fn.superfish;sf.o=[];sf.op={};sf.IE7fix=function(){var o=sf.op;if($.browser.msie&&$.browser.version>6&&o.dropShadows&&o.animation.opacity!=undefined)
this.toggleClass(sf.c.shadowClass+'-off');};sf.c={bcClass:'sf-breadcrumb',menuClass:'sf-js-enabled',anchorClass:'sf-with-ul',arrowClass:'sf-sub-indicator',shadowClass:'sf-shadow'};sf.defaults={hoverClass:'sfHover',pathClass:'overideThisToUse',pathLevels:1,delay:800,animation:{opacity:'show'},speed:'normal',autoArrows:true,dropShadows:true,disableHI:false,onInit:function(){},onBeforeShow:function(){},onShow:function(){},onHide:function(){}};$.fn.extend({hideSuperfishUl:function(){var o=sf.op,not=(o.retainPath===true)?o.$path:'';o.retainPath=false;var $ul=$(['li.',o.hoverClass].join(''),this).add(this).not(not).removeClass(o.hoverClass).find('>ul').hide().css('visibility','hidden');o.onHide.call($ul);return this;},showSuperfishUl:function(){var o=sf.op,sh=sf.c.shadowClass+'-off',$ul=this.addClass(o.hoverClass).find('>ul:hidden').css('visibility','visible');sf.IE7fix.call($ul);o.onBeforeShow.call($ul);$ul.animate(o.animation,o.speed,function(){sf.IE7fix.call($ul);o.onShow.call($ul);});return this;}});})(jQuery);(function($){$.extend($.ui,{datepicker:{version:"@VERSION"}});var PROP_NAME='datepicker';function Datepicker(){this.debug=false;this._curInst=null;this._keyEvent=false;this._disabledInputs=[];this._datepickerShowing=false;this._inDialog=false;this._mainDivId='ui-datepicker-div';this._inlineClass='ui-datepicker-inline';this._appendClass='ui-datepicker-append';this._triggerClass='ui-datepicker-trigger';this._dialogClass='ui-datepicker-dialog';this._disableClass='ui-datepicker-disabled';this._unselectableClass='ui-datepicker-unselectable';this._currentClass='ui-datepicker-current-day';this._dayOverClass='ui-datepicker-days-cell-over';this.regional=[];this.regional['']={closeText:'Done',prevText:'Prev',nextText:'Next',currentText:'Today',monthNames:['January','February','March','April','May','June','July','August','September','October','November','December'],monthNamesShort:['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],dayNames:['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],dayNamesShort:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],dayNamesMin:['Su','Mo','Tu','We','Th','Fr','Sa'],dateFormat:'mm/dd/yy',firstDay:0,isRTL:false,showMonthAfterYear:false,yearSuffix:''};this._defaults={showOn:'focus',showAnim:'show',showOptions:{},defaultDate:null,appendText:'',buttonText:'...',buttonImage:'',buttonImageOnly:false,hideIfNoPrevNext:false,navigationAsDateFormat:false,gotoCurrent:false,changeMonth:false,changeYear:false,yearRange:'-10:+10',showOtherMonths:false,calculateWeek:this.iso8601Week,shortYearCutoff:'+10',minDate:null,maxDate:null,duration:'fast',beforeShowDay:null,beforeShow:null,onSelect:null,onChangeMonthYear:null,onClose:null,numberOfMonths:1,showCurrentAtPos:0,stepMonths:1,stepBigMonths:12,altField:'',altFormat:'',constrainInput:true,showButtonPanel:false};$.extend(this._defaults,this.regional['']);this.dpDiv=$('<div id="'+this._mainDivId+'" class="ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all ui-helper-hidden-accessible"></div>');}
$.extend(Datepicker.prototype,{markerClassName:'hasDatepicker',log:function(){if(this.debug)
console.log.apply('',arguments);},setDefaults:function(settings){extendRemove(this._defaults,settings||{});return this;},_attachDatepicker:function(target,settings){var inlineSettings=null;for(var attrName in this._defaults){var attrValue=target.getAttribute('date:'+attrName);if(attrValue){inlineSettings=inlineSettings||{};try{inlineSettings[attrName]=eval(attrValue);}catch(err){inlineSettings[attrName]=attrValue;}}}
var nodeName=target.nodeName.toLowerCase();var inline=(nodeName=='div'||nodeName=='span');if(!target.id)
target.id='dp'+(++this.uuid);var inst=this._newInst($(target),inline);inst.settings=$.extend({},settings||{},inlineSettings||{});if(nodeName=='input'){this._connectDatepicker(target,inst);}else if(inline){this._inlineDatepicker(target,inst);}},_newInst:function(target,inline){var id=target[0].id.replace(/([:\[\]\.])/g,'\\\\$1');return{id:id,input:target,selectedDay:0,selectedMonth:0,selectedYear:0,drawMonth:0,drawYear:0,inline:inline,dpDiv:(!inline?this.dpDiv:$('<div class="'+this._inlineClass+' ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all"></div>'))};},_connectDatepicker:function(target,inst){var input=$(target);inst.append=$([]);inst.trigger=$([]);if(input.hasClass(this.markerClassName))
return;var appendText=this._get(inst,'appendText');var isRTL=this._get(inst,'isRTL');if(appendText){inst.append=$('<span class="'+this._appendClass+'">'+appendText+'</span>');input[isRTL?'before':'after'](inst.append);}
var showOn=this._get(inst,'showOn');if(showOn=='focus'||showOn=='both')
input.focus(this._showDatepicker);if(showOn=='button'||showOn=='both'){var buttonText=this._get(inst,'buttonText');var buttonImage=this._get(inst,'buttonImage');inst.trigger=$(this._get(inst,'buttonImageOnly')?$('<img/>').addClass(this._triggerClass).attr({src:buttonImage,alt:buttonText,title:buttonText}):$('<button type="button"></button>').addClass(this._triggerClass).html(buttonImage==''?buttonText:$('<img/>').attr({src:buttonImage,alt:buttonText,title:buttonText})));input[isRTL?'before':'after'](inst.trigger);inst.trigger.click(function(){if($.datepicker._datepickerShowing&&$.datepicker._lastInput==target)
$.datepicker._hideDatepicker();else
$.datepicker._showDatepicker(target);return false;});}
input.addClass(this.markerClassName).keydown(this._doKeyDown).keypress(this._doKeyPress).keyup(this._doKeyUp).bind("setData.datepicker",function(event,key,value){inst.settings[key]=value;}).bind("getData.datepicker",function(event,key){return this._get(inst,key);});$.data(target,PROP_NAME,inst);},_inlineDatepicker:function(target,inst){var divSpan=$(target);if(divSpan.hasClass(this.markerClassName))
return;divSpan.addClass(this.markerClassName).append(inst.dpDiv).bind("setData.datepicker",function(event,key,value){inst.settings[key]=value;}).bind("getData.datepicker",function(event,key){return this._get(inst,key);});$.data(target,PROP_NAME,inst);this._setDate(inst,this._getDefaultDate(inst));this._updateDatepicker(inst);this._updateAlternate(inst);},_dialogDatepicker:function(input,dateText,onSelect,settings,pos){var inst=this._dialogInst;if(!inst){var id='dp'+(++this.uuid);this._dialogInput=$('<input type="text" id="'+id+'" size="1" style="position: absolute; top: -100px;"/>');this._dialogInput.keydown(this._doKeyDown);$('body').append(this._dialogInput);inst=this._dialogInst=this._newInst(this._dialogInput,false);inst.settings={};$.data(this._dialogInput[0],PROP_NAME,inst);}
extendRemove(inst.settings,settings||{});this._dialogInput.val(dateText);this._pos=(pos?(pos.length?pos:[pos.pageX,pos.pageY]):null);if(!this._pos){var browserWidth=document.documentElement.clientWidth;var browserHeight=document.documentElement.clientHeight;var scrollX=document.documentElement.scrollLeft||document.body.scrollLeft;var scrollY=document.documentElement.scrollTop||document.body.scrollTop;this._pos=[(browserWidth/2)-100+scrollX,(browserHeight/2)-150+scrollY];}
this._dialogInput.css('left',this._pos[0]+'px').css('top',this._pos[1]+'px');inst.settings.onSelect=onSelect;this._inDialog=true;this.dpDiv.addClass(this._dialogClass);this._showDatepicker(this._dialogInput[0]);if($.blockUI)
$.blockUI(this.dpDiv);$.data(this._dialogInput[0],PROP_NAME,inst);return this;},_destroyDatepicker:function(target){var $target=$(target);var inst=$.data(target,PROP_NAME);if(!$target.hasClass(this.markerClassName)){return;}
var nodeName=target.nodeName.toLowerCase();$.removeData(target,PROP_NAME);if(nodeName=='input'){inst.append.remove();inst.trigger.remove();$target.removeClass(this.markerClassName).unbind('focus',this._showDatepicker).unbind('keydown',this._doKeyDown).unbind('keypress',this._doKeyPress).unbind('keyup',this._doKeyUp);}else if(nodeName=='div'||nodeName=='span')
$target.removeClass(this.markerClassName).empty();},_enableDatepicker:function(target){var $target=$(target);var inst=$.data(target,PROP_NAME);if(!$target.hasClass(this.markerClassName)){return;}
var nodeName=target.nodeName.toLowerCase();if(nodeName=='input'){target.disabled=false;inst.trigger.filter('button').each(function(){this.disabled=false;}).end().filter('img').css({opacity:'1.0',cursor:''});}
else if(nodeName=='div'||nodeName=='span'){var inline=$target.children('.'+this._inlineClass);inline.children().removeClass('ui-state-disabled');}
this._disabledInputs=$.map(this._disabledInputs,function(value){return(value==target?null:value);});},_disableDatepicker:function(target){var $target=$(target);var inst=$.data(target,PROP_NAME);if(!$target.hasClass(this.markerClassName)){return;}
var nodeName=target.nodeName.toLowerCase();if(nodeName=='input'){target.disabled=true;inst.trigger.filter('button').each(function(){this.disabled=true;}).end().filter('img').css({opacity:'0.5',cursor:'default'});}
else if(nodeName=='div'||nodeName=='span'){var inline=$target.children('.'+this._inlineClass);inline.children().addClass('ui-state-disabled');}
this._disabledInputs=$.map(this._disabledInputs,function(value){return(value==target?null:value);});this._disabledInputs[this._disabledInputs.length]=target;},_isDisabledDatepicker:function(target){if(!target){return false;}
for(var i=0;i<this._disabledInputs.length;i++){if(this._disabledInputs[i]==target)
return true;}
return false;},_getInst:function(target){try{return $.data(target,PROP_NAME);}
catch(err){throw'Missing instance data for this datepicker';}},_optionDatepicker:function(target,name,value){var inst=this._getInst(target);if(arguments.length==2&&typeof name=='string'){return(name=='defaults'?$.extend({},$.datepicker._defaults):(inst?(name=='all'?$.extend({},inst.settings):this._get(inst,name)):null));}
var settings=name||{};if(typeof name=='string'){settings={};settings[name]=value;}
if(inst){if(this._curInst==inst){this._hideDatepicker(null);}
var date=this._getDateDatepicker(target);extendRemove(inst.settings,settings);this._setDateDatepicker(target,date);this._updateDatepicker(inst);}},_changeDatepicker:function(target,name,value){this._optionDatepicker(target,name,value);},_refreshDatepicker:function(target){var inst=this._getInst(target);if(inst){this._updateDatepicker(inst);}},_setDateDatepicker:function(target,date){var inst=this._getInst(target);if(inst){this._setDate(inst,date);this._updateDatepicker(inst);this._updateAlternate(inst);}},_getDateDatepicker:function(target){var inst=this._getInst(target);if(inst&&!inst.inline)
this._setDateFromField(inst);return(inst?this._getDate(inst):null);},_doKeyDown:function(event){var inst=$.datepicker._getInst(event.target);var handled=true;var isRTL=inst.dpDiv.is('.ui-datepicker-rtl');inst._keyEvent=true;if($.datepicker._datepickerShowing)
switch(event.keyCode){case 9:$.datepicker._hideDatepicker(null,'');break;case 13:var sel=$('td.'+$.datepicker._dayOverClass+', td.'+$.datepicker._currentClass,inst.dpDiv);if(sel[0])
$.datepicker._selectDay(event.target,inst.selectedMonth,inst.selectedYear,sel[0]);else
$.datepicker._hideDatepicker(null,$.datepicker._get(inst,'duration'));return false;break;case 27:$.datepicker._hideDatepicker(null,$.datepicker._get(inst,'duration'));break;case 33:$.datepicker._adjustDate(event.target,(event.ctrlKey?-$.datepicker._get(inst,'stepBigMonths'):-$.datepicker._get(inst,'stepMonths')),'M');break;case 34:$.datepicker._adjustDate(event.target,(event.ctrlKey?+$.datepicker._get(inst,'stepBigMonths'):+$.datepicker._get(inst,'stepMonths')),'M');break;case 35:if(event.ctrlKey||event.metaKey)$.datepicker._clearDate(event.target);handled=event.ctrlKey||event.metaKey;break;case 36:if(event.ctrlKey||event.metaKey)$.datepicker._gotoToday(event.target);handled=event.ctrlKey||event.metaKey;break;case 37:if(event.ctrlKey||event.metaKey)$.datepicker._adjustDate(event.target,(isRTL?+1:-1),'D');handled=event.ctrlKey||event.metaKey;if(event.originalEvent.altKey)$.datepicker._adjustDate(event.target,(event.ctrlKey?-$.datepicker._get(inst,'stepBigMonths'):-$.datepicker._get(inst,'stepMonths')),'M');break;case 38:if(event.ctrlKey||event.metaKey)$.datepicker._adjustDate(event.target,-7,'D');handled=event.ctrlKey||event.metaKey;break;case 39:if(event.ctrlKey||event.metaKey)$.datepicker._adjustDate(event.target,(isRTL?-1:+1),'D');handled=event.ctrlKey||event.metaKey;if(event.originalEvent.altKey)$.datepicker._adjustDate(event.target,(event.ctrlKey?+$.datepicker._get(inst,'stepBigMonths'):+$.datepicker._get(inst,'stepMonths')),'M');break;case 40:if(event.ctrlKey||event.metaKey)$.datepicker._adjustDate(event.target,+7,'D');handled=event.ctrlKey||event.metaKey;break;default:handled=false;}
else if(event.keyCode==36&&event.ctrlKey)
$.datepicker._showDatepicker(this);else{handled=false;}
if(handled){event.preventDefault();event.stopPropagation();}},_doKeyPress:function(event){var inst=$.datepicker._getInst(event.target);if($.datepicker._get(inst,'constrainInput')){var chars=$.datepicker._possibleChars($.datepicker._get(inst,'dateFormat'));var chr=String.fromCharCode(event.charCode==undefined?event.keyCode:event.charCode);return event.ctrlKey||(chr<' '||!chars||chars.indexOf(chr)>-1);}},_doKeyUp:function(event){var inst=$.datepicker._getInst(event.target);if(!$.datepicker._get(inst,'altField'))
return true;try{var date=$.datepicker.parseDate($.datepicker._get(inst,'dateFormat'),(inst.input?inst.input.val():null),$.datepicker._getFormatConfig(inst));if(date){$.datepicker._setDateFromField(inst);$.datepicker._updateAlternate(inst);$.datepicker._updateDatepicker(inst);}}
catch(event){$.datepicker.log(event);}
return true;},_showDatepicker:function(input){input=input.target||input;if(input.nodeName.toLowerCase()!='input')
input=$('input',input.parentNode)[0];if($.datepicker._isDisabledDatepicker(input)||$.datepicker._lastInput==input)
return;var inst=$.datepicker._getInst(input);var beforeShow=$.datepicker._get(inst,'beforeShow');extendRemove(inst.settings,(beforeShow?beforeShow.apply(input,[input,inst]):{}));$.datepicker._hideDatepicker(null,'');$.datepicker._lastInput=input;$.datepicker._setDateFromField(inst);if($.datepicker._inDialog)
input.value='';if(!$.datepicker._pos){$.datepicker._pos=$.datepicker._findPos(input);$.datepicker._pos[1]+=input.offsetHeight;}
var isFixed=false;$(input).parents().each(function(){isFixed|=$(this).css('position')=='fixed';return!isFixed;});if(isFixed&&$.browser.opera){$.datepicker._pos[0]-=document.documentElement.scrollLeft;$.datepicker._pos[1]-=document.documentElement.scrollTop;}
var offset={left:$.datepicker._pos[0],top:$.datepicker._pos[1]};$.datepicker._pos=null;inst.dpDiv.css({position:'absolute',display:'block',top:'-1000px'});$.datepicker._updateDatepicker(inst);offset=$.datepicker._checkOffset(inst,offset,isFixed);inst.dpDiv.css({position:($.datepicker._inDialog&&$.blockUI?'static':(isFixed?'fixed':'absolute')),display:'none',left:offset.left+'px',top:offset.top+'px'});if(!inst.inline){var showAnim=$.datepicker._get(inst,'showAnim')||'show';var duration=$.datepicker._get(inst,'duration');var postProcess=function(){$.datepicker._datepickerShowing=true;var borders=$.datepicker._getBorders(inst.dpDiv);inst.dpDiv.find('iframe.ui-datepicker-cover').css({left:-borders[0],top:-borders[1],width:inst.dpDiv.outerWidth(),height:inst.dpDiv.outerHeight()});};if($.effects&&$.effects[showAnim])
inst.dpDiv.show(showAnim,$.datepicker._get(inst,'showOptions'),duration,postProcess);else
inst.dpDiv[showAnim](duration,postProcess);if(duration=='')
postProcess();if(inst.input[0].type!='hidden')
inst.input[0].focus();$.datepicker._curInst=inst;}},_updateDatepicker:function(inst){var self=this;var borders=$.datepicker._getBorders(inst.dpDiv);inst.dpDiv.empty().append(this._generateHTML(inst)).find('iframe.ui-datepicker-cover').css({left:-borders[0],top:-borders[1],width:inst.dpDiv.outerWidth(),height:inst.dpDiv.outerHeight()}).end().find('button, .ui-datepicker-prev, .ui-datepicker-next, .ui-datepicker-calendar td a').bind('mouseout',function(){$(this).removeClass('ui-state-hover');if(this.className.indexOf('ui-datepicker-prev')!=-1)$(this).removeClass('ui-datepicker-prev-hover');if(this.className.indexOf('ui-datepicker-next')!=-1)$(this).removeClass('ui-datepicker-next-hover');}).bind('mouseover',function(){if(!self._isDisabledDatepicker(inst.inline?inst.dpDiv.parent()[0]:inst.input[0])){$(this).parents('.ui-datepicker-calendar').find('a').removeClass('ui-state-hover');$(this).addClass('ui-state-hover');if(this.className.indexOf('ui-datepicker-prev')!=-1)$(this).addClass('ui-datepicker-prev-hover');if(this.className.indexOf('ui-datepicker-next')!=-1)$(this).addClass('ui-datepicker-next-hover');}}).end().find('.'+this._dayOverClass+' a').trigger('mouseover').end();var numMonths=this._getNumberOfMonths(inst);var cols=numMonths[1];var width=17;if(cols>1)
inst.dpDiv.addClass('ui-datepicker-multi-'+cols).css('width',(width*cols)+'em');else
inst.dpDiv.removeClass('ui-datepicker-multi-2 ui-datepicker-multi-3 ui-datepicker-multi-4').width('');inst.dpDiv[(numMonths[0]!=1||numMonths[1]!=1?'add':'remove')+'Class']('ui-datepicker-multi');inst.dpDiv[(this._get(inst,'isRTL')?'add':'remove')+'Class']('ui-datepicker-rtl');if(inst.input&&inst.input[0].type!='hidden'&&inst==$.datepicker._curInst)
$(inst.input[0]).focus();},_getBorders:function(elem){var convert=function(value){return{thin:1,medium:2,thick:3}[value]||value;};return[parseFloat(convert(elem.css('border-left-width'))),parseFloat(convert(elem.css('border-top-width')))];},_checkOffset:function(inst,offset,isFixed){var dpWidth=inst.dpDiv.outerWidth();var dpHeight=inst.dpDiv.outerHeight();var inputWidth=inst.input?inst.input.outerWidth():0;var inputHeight=inst.input?inst.input.outerHeight():0;var viewWidth=document.documentElement.clientWidth+$(document).scrollLeft();var viewHeight=document.documentElement.clientHeight+$(document).scrollTop();offset.left-=(this._get(inst,'isRTL')?(dpWidth-inputWidth):0);offset.left-=(isFixed&&offset.left==inst.input.offset().left)?$(document).scrollLeft():0;offset.top-=(isFixed&&offset.top==(inst.input.offset().top+inputHeight))?$(document).scrollTop():0;offset.left-=(offset.left+dpWidth>viewWidth&&viewWidth>dpWidth)?Math.abs(offset.left+dpWidth-viewWidth):0;offset.top-=(offset.top+dpHeight>viewHeight&&viewHeight>dpHeight)?Math.abs(offset.top+dpHeight+inputHeight*2-viewHeight):0;return offset;},_findPos:function(obj){while(obj&&(obj.type=='hidden'||obj.nodeType!=1)){obj=obj.nextSibling;}
var position=$(obj).offset();return[position.left,position.top];},_hideDatepicker:function(input,duration){var inst=this._curInst;if(!inst||(input&&inst!=$.data(input,PROP_NAME)))
return;if(this._datepickerShowing){duration=(duration!=null?duration:this._get(inst,'duration'));var showAnim=this._get(inst,'showAnim');var postProcess=function(){$.datepicker._tidyDialog(inst);};if(duration!=''&&$.effects&&$.effects[showAnim])
inst.dpDiv.hide(showAnim,$.datepicker._get(inst,'showOptions'),duration,postProcess);else
inst.dpDiv[(duration==''?'hide':(showAnim=='slideDown'?'slideUp':(showAnim=='fadeIn'?'fadeOut':'hide')))](duration,postProcess);if(duration=='')
this._tidyDialog(inst);var onClose=this._get(inst,'onClose');if(onClose)
onClose.apply((inst.input?inst.input[0]:null),[(inst.input?inst.input.val():''),inst]);this._datepickerShowing=false;this._lastInput=null;if(this._inDialog){this._dialogInput.css({position:'absolute',left:'0',top:'-100px'});if($.blockUI){$.unblockUI();$('body').append(this.dpDiv);}}
this._inDialog=false;}
this._curInst=null;},_tidyDialog:function(inst){inst.dpDiv.removeClass(this._dialogClass).unbind('.ui-datepicker-calendar');},_checkExternalClick:function(event){if(!$.datepicker._curInst)
return;var $target=$(event.target);if(($target.parents('#'+$.datepicker._mainDivId).length==0)&&!$target.hasClass($.datepicker.markerClassName)&&!$target.hasClass($.datepicker._triggerClass)&&$.datepicker._datepickerShowing&&!($.datepicker._inDialog&&$.blockUI))
$.datepicker._hideDatepicker(null,'');},_adjustDate:function(id,offset,period){var target=$(id);var inst=this._getInst(target[0]);if(this._isDisabledDatepicker(target[0])){return;}
this._adjustInstDate(inst,offset+
(period=='M'?this._get(inst,'showCurrentAtPos'):0),period);this._updateDatepicker(inst);},_gotoToday:function(id){var target=$(id);var inst=this._getInst(target[0]);if(this._get(inst,'gotoCurrent')&&inst.currentDay){inst.selectedDay=inst.currentDay;inst.drawMonth=inst.selectedMonth=inst.currentMonth;inst.drawYear=inst.selectedYear=inst.currentYear;}
else{var date=new Date();inst.selectedDay=date.getDate();inst.drawMonth=inst.selectedMonth=date.getMonth();inst.drawYear=inst.selectedYear=date.getFullYear();}
this._notifyChange(inst);this._adjustDate(target);},_selectMonthYear:function(id,select,period){var target=$(id);var inst=this._getInst(target[0]);inst._selectingMonthYear=false;inst['selected'+(period=='M'?'Month':'Year')]=inst['draw'+(period=='M'?'Month':'Year')]=parseInt(select.options[select.selectedIndex].value,10);this._notifyChange(inst);this._adjustDate(target);},_clickMonthYear:function(id){var target=$(id);var inst=this._getInst(target[0]);if(inst.input&&inst._selectingMonthYear&&!$.browser.msie)
inst.input[0].focus();inst._selectingMonthYear=!inst._selectingMonthYear;},_selectDay:function(id,month,year,td){var target=$(id);if($(td).hasClass(this._unselectableClass)||this._isDisabledDatepicker(target[0])){return;}
var inst=this._getInst(target[0]);inst.selectedDay=inst.currentDay=$('a',td).html();inst.selectedMonth=inst.currentMonth=month;inst.selectedYear=inst.currentYear=year;this._selectDate(id,this._formatDate(inst,inst.currentDay,inst.currentMonth,inst.currentYear));},_clearDate:function(id){var target=$(id);var inst=this._getInst(target[0]);this._selectDate(target,'');},_selectDate:function(id,dateStr){var target=$(id);var inst=this._getInst(target[0]);dateStr=(dateStr!=null?dateStr:this._formatDate(inst));if(inst.input)
inst.input.val(dateStr);this._updateAlternate(inst);var onSelect=this._get(inst,'onSelect');if(onSelect)
onSelect.apply((inst.input?inst.input[0]:null),[dateStr,inst]);else if(inst.input)
inst.input.trigger('change');if(inst.inline)
this._updateDatepicker(inst);else{this._hideDatepicker(null,this._get(inst,'duration'));this._lastInput=inst.input[0];if(typeof(inst.input[0])!='object')
inst.input[0].focus();this._lastInput=null;}},_updateAlternate:function(inst){var altField=this._get(inst,'altField');if(altField){var altFormat=this._get(inst,'altFormat')||this._get(inst,'dateFormat');var date=this._getDate(inst);dateStr=this.formatDate(altFormat,date,this._getFormatConfig(inst));$(altField).each(function(){$(this).val(dateStr);});}},noWeekends:function(date){var day=date.getDay();return[(day>0&&day<6),''];},iso8601Week:function(date){var checkDate=new Date(date.getTime());checkDate.setDate(checkDate.getDate()+4-(checkDate.getDay()||7));var time=checkDate.getTime();checkDate.setMonth(0);checkDate.setDate(1);return Math.floor(Math.round((time-checkDate)/86400000)/7)+1;},parseDate:function(format,value,settings){if(format==null||value==null)
throw'Invalid arguments';value=(typeof value=='object'?value.toString():value+'');if(value=='')
return null;var shortYearCutoff=(settings?settings.shortYearCutoff:null)||this._defaults.shortYearCutoff;var dayNamesShort=(settings?settings.dayNamesShort:null)||this._defaults.dayNamesShort;var dayNames=(settings?settings.dayNames:null)||this._defaults.dayNames;var monthNamesShort=(settings?settings.monthNamesShort:null)||this._defaults.monthNamesShort;var monthNames=(settings?settings.monthNames:null)||this._defaults.monthNames;var year=-1;var month=-1;var day=-1;var doy=-1;var literal=false;var lookAhead=function(match){var matches=(iFormat+1<format.length&&format.charAt(iFormat+1)==match);if(matches)
iFormat++;return matches;};var getNumber=function(match){lookAhead(match);var size=(match=='@'?14:(match=='!'?20:(match=='y'?4:(match=='o'?3:2))));var digits=new RegExp('^\\d{1,'+size+'}');var num=value.substring(iValue).match(digits);if(!num)
throw'Missing number at position '+iValue;iValue+=num[0].length;return parseInt(num[0],10);};var getName=function(match,shortNames,longNames){var names=(lookAhead(match)?longNames:shortNames);for(var i=0;i<names.length;i++){if(value.substr(iValue,names[i].length)==names[i]){iValue+=names[i].length;return i+1;}}
throw'Unknown name at position '+iValue;};var checkLiteral=function(){if(value.charAt(iValue)!=format.charAt(iFormat))
throw'Unexpected literal at position '+iValue;iValue++;};var iValue=0;for(var iFormat=0;iFormat<format.length;iFormat++){if(literal)
if(format.charAt(iFormat)=="'"&&!lookAhead("'"))
literal=false;else
checkLiteral();else
switch(format.charAt(iFormat)){case'd':day=getNumber('d');break;case'D':getName('D',dayNamesShort,dayNames);break;case'o':doy=getNumber('o');break;case'm':month=getNumber('m');break;case'M':month=getName('M',monthNamesShort,monthNames);break;case'y':year=getNumber('y');break;case'@':var date=new Date(getNumber('@'));year=date.getFullYear();month=date.getMonth()+1;day=date.getDate();break;case'!':var date=new Date((getNumber('!')-this._ticksTo1970)/10000);year=date.getFullYear();month=date.getMonth()+1;day=date.getDate();break;case"'":if(lookAhead("'"))
checkLiteral();else
literal=true;break;default:checkLiteral();}}
if(year==-1)
year=new Date().getFullYear();else if(year<100)
year+=new Date().getFullYear()-new Date().getFullYear()%100+
(year<=shortYearCutoff?0:-100);if(doy>-1){month=1;day=doy;do{var dim=this._getDaysInMonth(year,month-1);if(day<=dim)
break;month++;day-=dim;}while(true);}
var date=this._daylightSavingAdjust(new Date(year,month-1,day));if(date.getFullYear()!=year||date.getMonth()+1!=month||date.getDate()!=day)
throw'Invalid date';return date;},ATOM:'yy-mm-dd',COOKIE:'D, dd M yy',ISO_8601:'yy-mm-dd',RFC_822:'D, d M y',RFC_850:'DD, dd-M-y',RFC_1036:'D, d M y',RFC_1123:'D, d M yy',RFC_2822:'D, d M yy',RSS:'D, d M y',TICKS:'!',TIMESTAMP:'@',W3C:'yy-mm-dd',_ticksTo1970:(((1970-1)*365+Math.floor(1970/4)-Math.floor(1970/100)+
Math.floor(1970/400))*24*60*60*10000000),formatDate:function(format,date,settings){if(!date)
return'';var dayNamesShort=(settings?settings.dayNamesShort:null)||this._defaults.dayNamesShort;var dayNames=(settings?settings.dayNames:null)||this._defaults.dayNames;var monthNamesShort=(settings?settings.monthNamesShort:null)||this._defaults.monthNamesShort;var monthNames=(settings?settings.monthNames:null)||this._defaults.monthNames;var lookAhead=function(match){var matches=(iFormat+1<format.length&&format.charAt(iFormat+1)==match);if(matches)
iFormat++;return matches;};var formatNumber=function(match,value,len){var num=''+value;if(lookAhead(match))
while(num.length<len)
num='0'+num;return num;};var formatName=function(match,value,shortNames,longNames){return(lookAhead(match)?longNames[value]:shortNames[value]);};var output='';var literal=false;if(date)
for(var iFormat=0;iFormat<format.length;iFormat++){if(literal)
if(format.charAt(iFormat)=="'"&&!lookAhead("'"))
literal=false;else
output+=format.charAt(iFormat);else
switch(format.charAt(iFormat)){case'd':output+=formatNumber('d',date.getDate(),2);break;case'D':output+=formatName('D',date.getDay(),dayNamesShort,dayNames);break;case'o':output+=formatNumber('o',(date.getTime()-new Date(date.getFullYear(),0,0).getTime())/86400000,3);break;case'm':output+=formatNumber('m',date.getMonth()+1,2);break;case'M':output+=formatName('M',date.getMonth(),monthNamesShort,monthNames);break;case'y':output+=(lookAhead('y')?date.getFullYear():(date.getYear()%100<10?'0':'')+date.getYear()%100);break;case'@':output+=date.getTime();break;case'!':output+=date.getTime()*10000+this._ticksTo1970;break;case"'":if(lookAhead("'"))
output+="'";else
literal=true;break;default:output+=format.charAt(iFormat);}}
return output;},_possibleChars:function(format){var chars='';var literal=false;for(var iFormat=0;iFormat<format.length;iFormat++)
if(literal)
if(format.charAt(iFormat)=="'"&&!lookAhead("'"))
literal=false;else
chars+=format.charAt(iFormat);else
switch(format.charAt(iFormat)){case'd':case'm':case'y':case'@':chars+='0123456789';break;case'D':case'M':return null;case"'":if(lookAhead("'"))
chars+="'";else
literal=true;break;default:chars+=format.charAt(iFormat);}
return chars;},_get:function(inst,name){return inst.settings[name]!==undefined?inst.settings[name]:this._defaults[name];},_setDateFromField:function(inst){var dateFormat=this._get(inst,'dateFormat');var dates=inst.input?inst.input.val():null;var date=defaultDate=this._getDefaultDate(inst);var settings=this._getFormatConfig(inst);try{date=this.parseDate(dateFormat,dates,settings)||defaultDate;}catch(event){this.log(event);date=defaultDate;}
inst.selectedDay=date.getDate();inst.drawMonth=inst.selectedMonth=date.getMonth();inst.drawYear=inst.selectedYear=date.getFullYear();inst.currentDay=(dates?date.getDate():0);inst.currentMonth=(dates?date.getMonth():0);inst.currentYear=(dates?date.getFullYear():0);this._adjustInstDate(inst);},_getDefaultDate:function(inst){return this._restrictMinMax(inst,this._determineDate(this._get(inst,'defaultDate'),new Date()));},_determineDate:function(date,defaultDate){var offsetNumeric=function(offset){var date=new Date();date.setDate(date.getDate()+offset);return date;};var offsetString=function(offset,getDaysInMonth){var date=new Date();var year=date.getFullYear();var month=date.getMonth();var day=date.getDate();var pattern=/([+-]?[0-9]+)\s*(d|D|w|W|m|M|y|Y)?/g;var matches=pattern.exec(offset);while(matches){switch(matches[2]||'d'){case'd':case'D':day+=parseInt(matches[1],10);break;case'w':case'W':day+=parseInt(matches[1],10)*7;break;case'm':case'M':month+=parseInt(matches[1],10);day=Math.min(day,getDaysInMonth(year,month));break;case'y':case'Y':year+=parseInt(matches[1],10);day=Math.min(day,getDaysInMonth(year,month));break;}
matches=pattern.exec(offset);}
return new Date(year,month,day);};date=(date==null?defaultDate:(typeof date=='string'?offsetString(date,this._getDaysInMonth):(typeof date=='number'?(isNaN(date)?defaultDate:offsetNumeric(date)):date)));date=(date&&date.toString()=='Invalid Date'?defaultDate:date);if(date){date.setHours(0);date.setMinutes(0);date.setSeconds(0);date.setMilliseconds(0);}
return this._daylightSavingAdjust(date);},_daylightSavingAdjust:function(date){if(!date)return null;date.setHours(date.getHours()>12?date.getHours()+2:0);return date;},_setDate:function(inst,date){var clear=!(date);var origMonth=inst.selectedMonth;var origYear=inst.selectedYear;date=this._restrictMinMax(inst,this._determineDate(date,new Date()));inst.selectedDay=inst.currentDay=date.getDate();inst.drawMonth=inst.selectedMonth=inst.currentMonth=date.getMonth();inst.drawYear=inst.selectedYear=inst.currentYear=date.getFullYear();if(origMonth!=inst.selectedMonth||origYear!=inst.selectedYear)
this._notifyChange(inst);this._adjustInstDate(inst);if(inst.input){inst.input.val(clear?'':this._formatDate(inst));}},_getDate:function(inst){var startDate=(!inst.currentYear||(inst.input&&inst.input.val()=='')?null:this._daylightSavingAdjust(new Date(inst.currentYear,inst.currentMonth,inst.currentDay)));return startDate;},_generateHTML:function(inst){var today=new Date();today=this._daylightSavingAdjust(new Date(today.getFullYear(),today.getMonth(),today.getDate()));var isRTL=this._get(inst,'isRTL');var showButtonPanel=this._get(inst,'showButtonPanel');var hideIfNoPrevNext=this._get(inst,'hideIfNoPrevNext');var navigationAsDateFormat=this._get(inst,'navigationAsDateFormat');var numMonths=this._getNumberOfMonths(inst);var showCurrentAtPos=this._get(inst,'showCurrentAtPos');var stepMonths=this._get(inst,'stepMonths');var isMultiMonth=(numMonths[0]!=1||numMonths[1]!=1);var currentDate=this._daylightSavingAdjust((!inst.currentDay?new Date(9999,9,9):new Date(inst.currentYear,inst.currentMonth,inst.currentDay)));var minDate=this._getMinMaxDate(inst,'min');var maxDate=this._getMinMaxDate(inst,'max');var drawMonth=inst.drawMonth-showCurrentAtPos;var drawYear=inst.drawYear;if(drawMonth<0){drawMonth+=12;drawYear--;}
if(maxDate){var maxDraw=this._daylightSavingAdjust(new Date(maxDate.getFullYear(),maxDate.getMonth()-numMonths[1]+1,maxDate.getDate()));maxDraw=(minDate&&maxDraw<minDate?minDate:maxDraw);while(this._daylightSavingAdjust(new Date(drawYear,drawMonth,1))>maxDraw){drawMonth--;if(drawMonth<0){drawMonth=11;drawYear--;}}}
inst.drawMonth=drawMonth;inst.drawYear=drawYear;var prevText=this._get(inst,'prevText');prevText=(!navigationAsDateFormat?prevText:this.formatDate(prevText,this._daylightSavingAdjust(new Date(drawYear,drawMonth-stepMonths,1)),this._getFormatConfig(inst)));var prev=(this._canAdjustMonth(inst,-1,drawYear,drawMonth)?'<a class="ui-datepicker-prev ui-corner-all" onclick="DP_jQuery.datepicker._adjustDate(\'#'+inst.id+'\', -'+stepMonths+', \'M\');"'+' title="'+prevText+'"><span class="ui-icon ui-icon-circle-triangle-'+(isRTL?'e':'w')+'">'+prevText+'</span></a>':(hideIfNoPrevNext?'':'<a class="ui-datepicker-prev ui-corner-all ui-state-disabled" title="'+prevText+'"><span class="ui-icon ui-icon-circle-triangle-'+(isRTL?'e':'w')+'">'+prevText+'</span></a>'));var nextText=this._get(inst,'nextText');nextText=(!navigationAsDateFormat?nextText:this.formatDate(nextText,this._daylightSavingAdjust(new Date(drawYear,drawMonth+stepMonths,1)),this._getFormatConfig(inst)));var next=(this._canAdjustMonth(inst,+1,drawYear,drawMonth)?'<a class="ui-datepicker-next ui-corner-all" onclick="DP_jQuery.datepicker._adjustDate(\'#'+inst.id+'\', +'+stepMonths+', \'M\');"'+' title="'+nextText+'"><span class="ui-icon ui-icon-circle-triangle-'+(isRTL?'w':'e')+'">'+nextText+'</span></a>':(hideIfNoPrevNext?'':'<a class="ui-datepicker-next ui-corner-all ui-state-disabled" title="'+nextText+'"><span class="ui-icon ui-icon-circle-triangle-'+(isRTL?'w':'e')+'">'+nextText+'</span></a>'));var currentText=this._get(inst,'currentText');var gotoDate=(this._get(inst,'gotoCurrent')&&inst.currentDay?currentDate:today);currentText=(!navigationAsDateFormat?currentText:this.formatDate(currentText,gotoDate,this._getFormatConfig(inst)));var controls=(!inst.inline?'<button type="button" class="ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all" onclick="DP_jQuery.datepicker._hideDatepicker();">'+this._get(inst,'closeText')+'</button>':'');var buttonPanel=(showButtonPanel)?'<div class="ui-datepicker-buttonpane ui-widget-content">'+(isRTL?controls:'')+
(this._isInRange(inst,gotoDate)?'<button type="button" class="ui-datepicker-current ui-state-default ui-priority-secondary ui-corner-all" onclick="DP_jQuery.datepicker._gotoToday(\'#'+inst.id+'\');"'+'>'+currentText+'</button>':'')+(isRTL?'':controls)+'</div>':'';var firstDay=parseInt(this._get(inst,'firstDay'),10);firstDay=(isNaN(firstDay)?0:firstDay);var dayNames=this._get(inst,'dayNames');var dayNamesShort=this._get(inst,'dayNamesShort');var dayNamesMin=this._get(inst,'dayNamesMin');var monthNames=this._get(inst,'monthNames');var monthNamesShort=this._get(inst,'monthNamesShort');var beforeShowDay=this._get(inst,'beforeShowDay');var showOtherMonths=this._get(inst,'showOtherMonths');var calculateWeek=this._get(inst,'calculateWeek')||this.iso8601Week;var defaultDate=this._getDefaultDate(inst);var html='';for(var row=0;row<numMonths[0];row++){var group='';for(var col=0;col<numMonths[1];col++){var selectedDate=this._daylightSavingAdjust(new Date(drawYear,drawMonth,inst.selectedDay));var cornerClass=' ui-corner-all';var calender='';if(isMultiMonth){calender+='<div class="ui-datepicker-group ui-datepicker-group-';switch(col){case 0:calender+='first';cornerClass=' ui-corner-'+(isRTL?'right':'left');break;case numMonths[1]-1:calender+='last';cornerClass=' ui-corner-'+(isRTL?'left':'right');break;default:calender+='middle';cornerClass='';break;}
calender+='">';}
calender+='<div class="ui-datepicker-header ui-widget-header ui-helper-clearfix'+cornerClass+'">'+
(/all|left/.test(cornerClass)&&row==0?(isRTL?next:prev):'')+
(/all|right/.test(cornerClass)&&row==0?(isRTL?prev:next):'')+
this._generateMonthYearHeader(inst,drawMonth,drawYear,minDate,maxDate,row>0||col>0,monthNames,monthNamesShort)+'</div><table class="ui-datepicker-calendar"><thead>'+'<tr>';var thead='';for(var dow=0;dow<7;dow++){var day=(dow+firstDay)%7;thead+='<th'+((dow+firstDay+6)%7>=5?' class="ui-datepicker-week-end"':'')+'>'+'<span title="'+dayNames[day]+'">'+dayNamesMin[day]+'</span></th>';}
calender+=thead+'</tr></thead><tbody>';var daysInMonth=this._getDaysInMonth(drawYear,drawMonth);if(drawYear==inst.selectedYear&&drawMonth==inst.selectedMonth)
inst.selectedDay=Math.min(inst.selectedDay,daysInMonth);var leadDays=(this._getFirstDayOfMonth(drawYear,drawMonth)-firstDay+7)%7;var numRows=(isMultiMonth?6:Math.ceil((leadDays+daysInMonth)/7));var printDate=this._daylightSavingAdjust(new Date(drawYear,drawMonth,1-leadDays));for(var dRow=0;dRow<numRows;dRow++){calender+='<tr>';var tbody='';for(var dow=0;dow<7;dow++){var daySettings=(beforeShowDay?beforeShowDay.apply((inst.input?inst.input[0]:null),[printDate]):[true,'']);var otherMonth=(printDate.getMonth()!=drawMonth);var unselectable=otherMonth||!daySettings[0]||(minDate&&printDate<minDate)||(maxDate&&printDate>maxDate);tbody+='<td class="'+
((dow+firstDay+6)%7>=5?' ui-datepicker-week-end':'')+
(otherMonth?' ui-datepicker-other-month':'')+
((printDate.getTime()==selectedDate.getTime()&&drawMonth==inst.selectedMonth&&inst._keyEvent)||(defaultDate.getTime()==printDate.getTime()&&defaultDate.getTime()==selectedDate.getTime())?' '+this._dayOverClass:'')+
(unselectable?' '+this._unselectableClass+' ui-state-disabled':'')+
(otherMonth&&!showOtherMonths?'':' '+daySettings[1]+
(printDate.getTime()==currentDate.getTime()?' '+this._currentClass:'')+
(printDate.getTime()==today.getTime()?' ui-datepicker-today':''))+'"'+
((!otherMonth||showOtherMonths)&&daySettings[2]?' title="'+daySettings[2]+'"':'')+
(unselectable?'':' onclick="DP_jQuery.datepicker._selectDay(\'#'+
inst.id+'\','+drawMonth+','+drawYear+', this);return false;"')+'>'+
(otherMonth?(showOtherMonths?printDate.getDate():'&#xa0;'):(unselectable?'<span class="ui-state-default">'+printDate.getDate()+'</span>':'<a class="ui-state-default'+
(printDate.getTime()==today.getTime()?' ui-state-highlight':'')+
(printDate.getTime()==currentDate.getTime()?' ui-state-active':'')+'" href="#">'+printDate.getDate()+'</a>'))+'</td>';printDate.setDate(printDate.getDate()+1);printDate=this._daylightSavingAdjust(printDate);}
calender+=tbody+'</tr>';}
drawMonth++;if(drawMonth>11){drawMonth=0;drawYear++;}
calender+='</tbody></table>'+(isMultiMonth?'</div>'+
((numMonths[0]>0&&col==numMonths[1]-1)?'<div class="ui-datepicker-row-break"></div>':''):'');group+=calender;}
html+=group;}
html+=buttonPanel+($.browser.msie&&parseInt($.browser.version,10)<7&&!inst.inline?'<iframe src="javascript:false;" class="ui-datepicker-cover" frameborder="0"></iframe>':'');inst._keyEvent=false;return html;},_generateMonthYearHeader:function(inst,drawMonth,drawYear,minDate,maxDate,secondary,monthNames,monthNamesShort){var changeMonth=this._get(inst,'changeMonth');var changeYear=this._get(inst,'changeYear');var showMonthAfterYear=this._get(inst,'showMonthAfterYear');var html='<div class="ui-datepicker-title">';var monthHtml='';if(secondary||!changeMonth)
monthHtml+='<span class="ui-datepicker-month">'+monthNames[drawMonth]+'</span> ';else{var inMinYear=(minDate&&minDate.getFullYear()==drawYear);var inMaxYear=(maxDate&&maxDate.getFullYear()==drawYear);monthHtml+='<select class="ui-datepicker-month" '+'onchange="DP_jQuery.datepicker._selectMonthYear(\'#'+inst.id+'\', this, \'M\');" '+'onclick="DP_jQuery.datepicker._clickMonthYear(\'#'+inst.id+'\');"'+'>';for(var month=0;month<12;month++){if((!inMinYear||month>=minDate.getMonth())&&(!inMaxYear||month<=maxDate.getMonth()))
monthHtml+='<option value="'+month+'"'+
(month==drawMonth?' selected="selected"':'')+'>'+monthNamesShort[month]+'</option>';}
monthHtml+='</select>';}
if(!showMonthAfterYear)
html+=monthHtml+((secondary||changeMonth||changeYear)&&(!(changeMonth&&changeYear))?'&#xa0;':'');if(secondary||!changeYear)
html+='<span class="ui-datepicker-year">'+drawYear+'</span>';else{var years=this._get(inst,'yearRange').split(':');var year=0;var endYear=0;if(years.length!=2){year=drawYear-10;endYear=drawYear+10;}else if(years[0].charAt(0)=='+'||years[0].charAt(0)=='-'){year=drawYear+parseInt(years[0],10);endYear=drawYear+parseInt(years[1],10);}else{year=parseInt(years[0],10);endYear=parseInt(years[1],10);}
year=(minDate?Math.max(year,minDate.getFullYear()):year);endYear=(maxDate?Math.min(endYear,maxDate.getFullYear()):endYear);html+='<select class="ui-datepicker-year" '+'onchange="DP_jQuery.datepicker._selectMonthYear(\'#'+inst.id+'\', this, \'Y\');" '+'onclick="DP_jQuery.datepicker._clickMonthYear(\'#'+inst.id+'\');"'+'>';for(;year<=endYear;year++){html+='<option value="'+year+'"'+
(year==drawYear?' selected="selected"':'')+'>'+year+'</option>';}
html+='</select>';}
html+=this._get(inst,'yearSuffix');if(showMonthAfterYear)
html+=(secondary||changeMonth||changeYear?'&#xa0;':'')+monthHtml;html+='</div>';return html;},_adjustInstDate:function(inst,offset,period){var year=inst.drawYear+(period=='Y'?offset:0);var month=inst.drawMonth+(period=='M'?offset:0);var day=Math.min(inst.selectedDay,this._getDaysInMonth(year,month))+
(period=='D'?offset:0);var date=this._restrictMinMax(inst,this._daylightSavingAdjust(new Date(year,month,day)));inst.selectedDay=date.getDate();inst.drawMonth=inst.selectedMonth=date.getMonth();inst.drawYear=inst.selectedYear=date.getFullYear();if(period=='M'||period=='Y')
this._notifyChange(inst);},_restrictMinMax:function(inst,date){var minDate=this._getMinMaxDate(inst,'min');var maxDate=this._getMinMaxDate(inst,'max');date=(minDate&&date<minDate?minDate:date);date=(maxDate&&date>maxDate?maxDate:date);return date;},_notifyChange:function(inst){var onChange=this._get(inst,'onChangeMonthYear');if(onChange)
onChange.apply((inst.input?inst.input[0]:null),[inst.selectedYear,inst.selectedMonth+1,inst]);},_getNumberOfMonths:function(inst){var numMonths=this._get(inst,'numberOfMonths');return(numMonths==null?[1,1]:(typeof numMonths=='number'?[1,numMonths]:numMonths));},_getMinMaxDate:function(inst,minMax){return this._determineDate(this._get(inst,minMax+'Date'),null);},_getDaysInMonth:function(year,month){return 32-new Date(year,month,32).getDate();},_getFirstDayOfMonth:function(year,month){return new Date(year,month,1).getDay();},_canAdjustMonth:function(inst,offset,curYear,curMonth){var numMonths=this._getNumberOfMonths(inst);var date=this._daylightSavingAdjust(new Date(curYear,curMonth+(offset<0?offset:numMonths[1]),1));if(offset<0)
date.setDate(this._getDaysInMonth(date.getFullYear(),date.getMonth()));return this._isInRange(inst,date);},_isInRange:function(inst,date){var minDate=this._getMinMaxDate(inst,'min');var maxDate=this._getMinMaxDate(inst,'max');return((!minDate||date>=minDate)&&(!maxDate||date<=maxDate));},_getFormatConfig:function(inst){var shortYearCutoff=this._get(inst,'shortYearCutoff');shortYearCutoff=(typeof shortYearCutoff!='string'?shortYearCutoff:new Date().getFullYear()%100+parseInt(shortYearCutoff,10));return{shortYearCutoff:shortYearCutoff,dayNamesShort:this._get(inst,'dayNamesShort'),dayNames:this._get(inst,'dayNames'),monthNamesShort:this._get(inst,'monthNamesShort'),monthNames:this._get(inst,'monthNames')};},_formatDate:function(inst,day,month,year){if(!day){inst.currentDay=inst.selectedDay;inst.currentMonth=inst.selectedMonth;inst.currentYear=inst.selectedYear;}
var date=(day?(typeof day=='object'?day:this._daylightSavingAdjust(new Date(year,month,day))):this._daylightSavingAdjust(new Date(inst.currentYear,inst.currentMonth,inst.currentDay)));return this.formatDate(this._get(inst,'dateFormat'),date,this._getFormatConfig(inst));}});function extendRemove(target,props){$.extend(target,props);for(var name in props)
if(props[name]==null||props[name]==undefined)
target[name]=props[name];return target;};function isArray(a){return(a&&(($.browser.safari&&typeof a=='object'&&a.length)||(a.constructor&&a.constructor.toString().match(/\Array\(\)/))));};$.fn.datepicker=function(options){if(!$.datepicker.initialized){$(document).mousedown($.datepicker._checkExternalClick).find('body').append($.datepicker.dpDiv);$.datepicker.initialized=true;}
var otherArgs=Array.prototype.slice.call(arguments,1);if(typeof options=='string'&&(options=='isDisabled'||options=='getDate'))
return $.datepicker['_'+options+'Datepicker'].apply($.datepicker,[this[0]].concat(otherArgs));if(options=='option'&&arguments.length==2&&typeof arguments[1]=='string')
return $.datepicker['_'+options+'Datepicker'].apply($.datepicker,[this[0]].concat(otherArgs));return this.each(function(){typeof options=='string'?$.datepicker['_'+options+'Datepicker'].apply($.datepicker,[this].concat(otherArgs)):$.datepicker._attachDatepicker(this,options);});};$.datepicker=new Datepicker();$.datepicker.initialized=false;$.datepicker.uuid=new Date().getTime();$.datepicker.version="@VERSION";window.DP_jQuery=$;})(jQuery);var fieldlimiter={defaultoutput:"<b>[int]</b> characters remaining in your input limit.",uncheckedkeycodes:/(8)|(13)|(16)|(17)|(18)|(32)/,limitinput:function(e,config){var e=window.event||e
var thefield=config.thefield
var keyunicode=e.charCode||e.keyCode
if(!this.uncheckedkeycodes.test(keyunicode)){if(navigator.userAgent.indexOf("Firefox")!=-1){var split=thefield.value.split("\n")
a=split.length-1}
else{a=0}
if(thefield.value.length+a>=config.maxlength){if(e.preventDefault)
e.preventDefault()
return false}}},showlimit:function(config){var thefield=config.thefield
var statusids=config.statusids
var charsleft
if(navigator.userAgent.indexOf("Firefox")!=-1)
{charsleft=config.maxlength-thefield.value.replace(/\n/g,"\r\n").length}
else{charsleft=config.maxlength-thefield.value.length}
if(charsleft<0)
if(navigator.userAgent.indexOf("Firefox")!=-1){var split=thefield.value.split("\n")
var a=split.length-1
thefield.value=thefield.value.substring(0,config.maxlength-a)}
else{thefield.value=thefield.value.substring(0,config.maxlength)}
for(var i=0;i<statusids.length;i++){var statusdiv=document.getElementById(statusids[i])
if(statusdiv)
statusdiv.innerHTML=this.defaultoutput.replace("[int]",Math.max(0,charsleft))}
config.onkeypress.call(thefield,config.maxlength,thefield.value.length)},cleanup:function(config){for(var prop in config){config[prop]=null}},addEvent:function(targetarr,functionref,tasktype){if(targetarr.length>0){var target=targetarr.shift()
if(target.addEventListener)
target.addEventListener(tasktype,functionref,false)
else if(target.attachEvent)
target.attachEvent('on'+tasktype,function(){return functionref.call(target,window.event)})
this.addEvent(targetarr,functionref,tasktype)}},setup:function(config){if(config.thefield){config.onkeypress=config.onkeypress||function(){}
config.thefield.value=config.thefield.value
this.showlimit(config)
this.addEvent([window],function(e){fieldlimiter.showlimit(config)},"load")
this.addEvent([window],function(e){fieldlimiter.cleanup(config)},"unload")
this.addEvent([config.thefield],function(e){return fieldlimiter.limitinput(e,config)},"keypress")
this.addEvent([config.thefield],function(){fieldlimiter.showlimit(config)},"keyup")}}}
jQuery.cookie=function(name,value,options){if(typeof value!='undefined'){options=options||{};if(value===null){value='';options.expires=-1;}
var expires='';if(options.expires&&(typeof options.expires=='number'||options.expires.toUTCString)){var date;if(typeof options.expires=='number'){date=new Date();date.setTime(date.getTime()+(options.expires*24*60*60*1000));}else{date=options.expires;}
expires='; expires='+date.toUTCString();}
var path=options.path?'; path='+(options.path):'';var domain=options.domain?'; domain='+(options.domain):'';var secure=options.secure?'; secure':'';document.cookie=[name,'=',encodeURIComponent(value),expires,path,domain,secure].join('');}else{var cookieValue=null;if(document.cookie&&document.cookie!=''){var cookies=document.cookie.split(';');for(var i=0;i<cookies.length;i++){var cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)==(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}};eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('(2($){$.c.f=2(p){p=$.d({g:"!@#$%^&*()+=[]\\\\\\\';,/{}|\\":<>?~`.- ",4:"",9:""},p);7 3.b(2(){5(p.G)p.4+="Q";5(p.w)p.4+="n";s=p.9.z(\'\');x(i=0;i<s.y;i++)5(p.g.h(s[i])!=-1)s[i]="\\\\"+s[i];p.9=s.O(\'|\');6 l=N M(p.9,\'E\');6 a=p.g+p.4;a=a.H(l,\'\');$(3).J(2(e){5(!e.r)k=o.q(e.K);L k=o.q(e.r);5(a.h(k)!=-1)e.j();5(e.u&&k==\'v\')e.j()});$(3).B(\'D\',2(){7 F})})};$.c.I=2(p){6 8="n";8+=8.P();p=$.d({4:8},p);7 3.b(2(){$(3).f(p)})};$.c.t=2(p){6 m="A";p=$.d({4:m},p);7 3.b(2(){$(3).f(p)})}})(C);',53,53,'||function|this|nchars|if|var|return|az|allow|ch|each|fn|extend||alphanumeric|ichars|indexOf||preventDefault||reg|nm|abcdefghijklmnopqrstuvwxyz|String||fromCharCode|charCode||alpha|ctrlKey||allcaps|for|length|split|1234567890|bind|jQuery|contextmenu|gi|false|nocaps|replace|numeric|keypress|which|else|RegExp|new|join|toUpperCase|ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('|'),0,{}));(function($){$.fn.hoverIntent=function(f,g){var cfg={sensitivity:7,interval:100,timeout:0};cfg=$.extend(cfg,g?{over:f,out:g}:f);var cX,cY,pX,pY;var track=function(ev){cX=ev.pageX;cY=ev.pageY;};var compare=function(ev,ob){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t);if((Math.abs(pX-cX)+Math.abs(pY-cY))<cfg.sensitivity){$(ob).unbind("mousemove",track);ob.hoverIntent_s=1;return cfg.over.apply(ob,[ev]);}else{pX=cX;pY=cY;ob.hoverIntent_t=setTimeout(function(){compare(ev,ob);},cfg.interval);}};var delay=function(ev,ob){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t);ob.hoverIntent_s=0;return cfg.out.apply(ob,[ev]);};var handleHover=function(e){var p=(e.type=="mouseover"?e.fromElement:e.toElement)||e.relatedTarget;while(p&&p!=this){try{p=p.parentNode;}catch(e){p=this;}}
if(p==this){return false;}
var ev=jQuery.extend({},e);var ob=this;if(ob.hoverIntent_t){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t);}
if(e.type=="mouseover"){pX=ev.pageX;pY=ev.pageY;$(ob).bind("mousemove",track);if(ob.hoverIntent_s!=1){ob.hoverIntent_t=setTimeout(function(){compare(ev,ob);},cfg.interval);}}else{$(ob).unbind("mousemove",track);if(ob.hoverIntent_s==1){ob.hoverIntent_t=setTimeout(function(){delay(ev,ob);},cfg.timeout);}}};return this.mouseover(handleHover).mouseout(handleHover);};})(jQuery);;(function($){$.fn.ajaxSubmit=function(options){if(!this.length){log('ajaxSubmit: skipping submit process - no element selected');return this;}
if(typeof options=='function')
options={success:options};options=$.extend({url:this.attr('action')||window.location.toString(),type:this.attr('method')||'GET'},options||{});var veto={};this.trigger('form-pre-serialize',[this,options,veto]);if(veto.veto){log('ajaxSubmit: submit vetoed via form-pre-serialize trigger');return this;}
if(options.beforeSerialize&&options.beforeSerialize(this,options)===false){log('ajaxSubmit: submit aborted via beforeSerialize callback');return this;}
var a=this.formToArray(options.semantic);if(options.data){options.extraData=options.data;for(var n in options.data){if(options.data[n]instanceof Array){for(var k in options.data[n])
a.push({name:n,value:options.data[n][k]})}
else
a.push({name:n,value:options.data[n]});}}
if(options.beforeSubmit&&options.beforeSubmit(a,this,options)===false){log('ajaxSubmit: submit aborted via beforeSubmit callback');return this;}
this.trigger('form-submit-validate',[a,this,options,veto]);if(veto.veto){log('ajaxSubmit: submit vetoed via form-submit-validate trigger');return this;}
var q=$.param(a);if(options.type.toUpperCase()=='GET'){options.url+=(options.url.indexOf('?')>=0?'&':'?')+q;options.data=null;}
else
options.data=q;var $form=this,callbacks=[];if(options.resetForm)callbacks.push(function(){$form.resetForm();});if(options.clearForm)callbacks.push(function(){$form.clearForm();});if(!options.dataType&&options.target){var oldSuccess=options.success||function(){};callbacks.push(function(data){$(options.target).html(data).each(oldSuccess,arguments);});}
else if(options.success)
callbacks.push(options.success);options.success=function(data,status){for(var i=0,max=callbacks.length;i<max;i++)
callbacks[i].apply(options,[data,status,$form]);};var files=$('input:file',this).fieldValue();var found=false;for(var j=0;j<files.length;j++)
if(files[j])
found=true;if(options.iframe||found){if(options.closeKeepAlive)
$.get(options.closeKeepAlive,fileUpload);else
fileUpload();}
else
$.ajax(options);this.trigger('form-submit-notify',[this,options]);return this;function fileUpload(){var form=$form[0];if($(':input[name=submit]',form).length){alert('Error: Form elements must not be named "submit".');return;}
var opts=$.extend({},$.ajaxSettings,options);var s=jQuery.extend(true,{},$.extend(true,{},$.ajaxSettings),opts);var id='jqFormIO'+(new Date().getTime());var $io=$('<iframe id="'+id+'" name="'+id+'" src="about:blank" />');var io=$io[0];$io.css({position:'absolute',top:'-1000px',left:'-1000px'});var xhr={aborted:0,responseText:null,responseXML:null,status:0,statusText:'n/a',getAllResponseHeaders:function(){},getResponseHeader:function(){},setRequestHeader:function(){},abort:function(){this.aborted=1;$io.attr('src','about:blank');}};var g=opts.global;if(g&&!$.active++)$.event.trigger("ajaxStart");if(g)$.event.trigger("ajaxSend",[xhr,opts]);if(s.beforeSend&&s.beforeSend(xhr,s)===false){s.global&&jQuery.active--;return;}
if(xhr.aborted)
return;var cbInvoked=0;var timedOut=0;var sub=form.clk;if(sub){var n=sub.name;if(n&&!sub.disabled){options.extraData=options.extraData||{};options.extraData[n]=sub.value;if(sub.type=="image"){options.extraData[name+'.x']=form.clk_x;options.extraData[name+'.y']=form.clk_y;}}}
setTimeout(function(){var t=$form.attr('target'),a=$form.attr('action');form.setAttribute('target',id);if(form.getAttribute('method')!='POST')
form.setAttribute('method','POST');if(form.getAttribute('action')!=opts.url)
form.setAttribute('action',opts.url);if(!options.skipEncodingOverride){$form.attr({encoding:'multipart/form-data',enctype:'multipart/form-data'});}
if(opts.timeout)
setTimeout(function(){timedOut=true;cb();},opts.timeout);var extraInputs=[];try{if(options.extraData)
for(var n in options.extraData)
extraInputs.push($('<input type="hidden" name="'+n+'" value="'+options.extraData[n]+'" />').appendTo(form)[0]);$io.appendTo('body');io.attachEvent?io.attachEvent('onload',cb):io.addEventListener('load',cb,false);form.submit();}
finally{form.setAttribute('action',a);t?form.setAttribute('target',t):$form.removeAttr('target');$(extraInputs).remove();}},10);var nullCheckFlag=0;function cb(){if(cbInvoked++)return;io.detachEvent?io.detachEvent('onload',cb):io.removeEventListener('load',cb,false);var ok=true;try{if(timedOut)throw'timeout';var data,doc;doc=io.contentWindow?io.contentWindow.document:io.contentDocument?io.contentDocument:io.document;if((doc.body==null||doc.body.innerHTML=='')&&!nullCheckFlag){nullCheckFlag=1;cbInvoked--;setTimeout(cb,100);return;}
xhr.responseText=doc.body?doc.body.innerHTML:null;xhr.responseXML=doc.XMLDocument?doc.XMLDocument:doc;xhr.getResponseHeader=function(header){var headers={'content-type':opts.dataType};return headers[header];};if(opts.dataType=='json'||opts.dataType=='script'){var ta=doc.getElementsByTagName('textarea')[0];xhr.responseText=ta?ta.value:xhr.responseText;}
else if(opts.dataType=='xml'&&!xhr.responseXML&&xhr.responseText!=null){xhr.responseXML=toXml(xhr.responseText);}
data=$.httpData(xhr,opts.dataType);}
catch(e){ok=false;$.handleError(opts,xhr,'error',e);}
if(ok){opts.success(data,'success');if(g)$.event.trigger("ajaxSuccess",[xhr,opts]);}
if(g)$.event.trigger("ajaxComplete",[xhr,opts]);if(g&&!--$.active)$.event.trigger("ajaxStop");if(opts.complete)opts.complete(xhr,ok?'success':'error');setTimeout(function(){$io.remove();xhr.responseXML=null;},100);};function toXml(s,doc){if(window.ActiveXObject){doc=new ActiveXObject('Microsoft.XMLDOM');doc.async='false';doc.loadXML(s);}
else
doc=(new DOMParser()).parseFromString(s,'text/xml');return(doc&&doc.documentElement&&doc.documentElement.tagName!='parsererror')?doc:null;};};};$.fn.ajaxForm=function(options){return this.ajaxFormUnbind().bind('submit.form-plugin',function(){$(this).ajaxSubmit(options);return false;}).each(function(){$(":submit,input:image",this).bind('click.form-plugin',function(e){var form=this.form;form.clk=this;if(this.type=='image'){if(e.offsetX!=undefined){form.clk_x=e.offsetX;form.clk_y=e.offsetY;}else if(typeof $.fn.offset=='function'){var offset=$(this).offset();form.clk_x=e.pageX-offset.left;form.clk_y=e.pageY-offset.top;}else{form.clk_x=e.pageX-this.offsetLeft;form.clk_y=e.pageY-this.offsetTop;}}
setTimeout(function(){form.clk=form.clk_x=form.clk_y=null;},10);});});};$.fn.ajaxFormUnbind=function(){this.unbind('submit.form-plugin');return this.each(function(){$(":submit,input:image",this).unbind('click.form-plugin');});};$.fn.formToArray=function(semantic){var a=[];if(this.length==0)return a;var form=this[0];var els=semantic?form.getElementsByTagName('*'):form.elements;if(!els)return a;for(var i=0,max=els.length;i<max;i++){var el=els[i];var n=el.name;if(!n)continue;if(semantic&&form.clk&&el.type=="image"){if(!el.disabled&&form.clk==el)
a.push({name:n+'.x',value:form.clk_x},{name:n+'.y',value:form.clk_y});continue;}
var v=$.fieldValue(el,true);if(v&&v.constructor==Array){for(var j=0,jmax=v.length;j<jmax;j++)
a.push({name:n,value:v[j]});}
else if(v!==null&&typeof v!='undefined')
a.push({name:n,value:v});}
if(!semantic&&form.clk){var inputs=form.getElementsByTagName("input");for(var i=0,max=inputs.length;i<max;i++){var input=inputs[i];var n=input.name;if(n&&!input.disabled&&input.type=="image"&&form.clk==input)
a.push({name:n+'.x',value:form.clk_x},{name:n+'.y',value:form.clk_y});}}
return a;};$.fn.formSerialize=function(semantic){return $.param(this.formToArray(semantic));};$.fn.fieldSerialize=function(successful){var a=[];this.each(function(){var n=this.name;if(!n)return;var v=$.fieldValue(this,successful);if(v&&v.constructor==Array){for(var i=0,max=v.length;i<max;i++)
a.push({name:n,value:v[i]});}
else if(v!==null&&typeof v!='undefined')
a.push({name:this.name,value:v});});return $.param(a);};$.fn.fieldValue=function(successful){for(var val=[],i=0,max=this.length;i<max;i++){var el=this[i];var v=$.fieldValue(el,successful);if(v===null||typeof v=='undefined'||(v.constructor==Array&&!v.length))
continue;v.constructor==Array?$.merge(val,v):val.push(v);}
return val;};$.fieldValue=function(el,successful){var n=el.name,t=el.type,tag=el.tagName.toLowerCase();if(typeof successful=='undefined')successful=true;if(successful&&(!n||el.disabled||t=='reset'||t=='button'||(t=='checkbox'||t=='radio')&&!el.checked||(t=='submit'||t=='image')&&el.form&&el.form.clk!=el||tag=='select'&&el.selectedIndex==-1))
return null;if(tag=='select'){var index=el.selectedIndex;if(index<0)return null;var a=[],ops=el.options;var one=(t=='select-one');var max=(one?index+1:ops.length);for(var i=(one?index:0);i<max;i++){var op=ops[i];if(op.selected){var v=op.value;if(!v)
v=(op.attributes&&op.attributes['value']&&!(op.attributes['value'].specified))?op.text:op.value;if(one)return v;a.push(v);}}
return a;}
return el.value;};$.fn.clearForm=function(){return this.each(function(){$('input,select,textarea',this).clearFields();});};$.fn.clearFields=$.fn.clearInputs=function(){return this.each(function(){var t=this.type,tag=this.tagName.toLowerCase();if(t=='text'||t=='password'||tag=='textarea')
this.value='';else if(t=='checkbox'||t=='radio')
this.checked=false;else if(tag=='select')
this.selectedIndex=-1;});};$.fn.resetForm=function(){return this.each(function(){if(typeof this.reset=='function'||(typeof this.reset=='object'&&!this.reset.nodeType))
this.reset();});};$.fn.enable=function(b){if(b==undefined)b=true;return this.each(function(){this.disabled=!b});};$.fn.selected=function(select){if(select==undefined)select=true;return this.each(function(){var t=this.type;if(t=='checkbox'||t=='radio')
this.checked=select;else if(this.tagName.toLowerCase()=='option'){var $sel=$(this).parent('select');if(select&&$sel[0]&&$sel[0].type=='select-one'){$sel.find('option').selected(false);}
this.selected=select;}});};function log(){if($.fn.ajaxSubmit.debug&&window.console&&window.console.log)
window.console.log('[jquery.form] '+Array.prototype.join.call(arguments,''));};})(jQuery);$.extend({'mobile':function(){return!$.browser.msie&&!$.browser.mozilla&&!$.browser.opera&&!$.browser.safari&&!$.browser.flock&&!$.browser.linux&&!$.browser.mac&&!$.browser.win}})
function searchFormTabs(arr0){var arr=arr0
var tabs_relative=$('<div id="search_form_tabs_relative">').html('&nbsp;')
var tabs_holder=$('<div id="search_form_tabs"></div>')
var tabs=$([])
var last_form=$([])
for(var i=0;i<arr.length;i++){var form=$('#'+arr[i].id)
if(form.length<1){alert('cannot find form '+arr[i].id)}
if(i==0){tabs_relative.insertBefore(form)
tabs_holder.appendTo(tabs_relative)
last_form=last_form.add(form)}
else{form.hide()}
var tab=$('<a></a>').attr('href','#').data('form',form).html(arr[i].text).click(function(e){e.preventDefault()
last_tab.removeClass('selected')
last_form.hide()
$(this).data('form').show()
$(this).addClass('selected')
last_tab=$(this)
last_form=$(this).data('form')
$.cookie('search_form',tabs.index(this),{path:'/'})}).appendTo(tabs_holder)
if(i==0){tab.addClass('selected')
last_tab=tab}
tabs=tabs.add(tab)}
if($.cookie('search_form')){tabs.eq($.cookie('search_form')).triggerHandler('click')}}
function updateModel2(json0){if(!typeof(json0)=='object'){alert('updatemodel2 - 1st argument must a json object')
return 0}
if(!typeof(json0.form)=='string'){alert('updatemodel2 - json object must have "form"')
return 0}
if(!typeof(json0.model)=='string'){alert('updatemodel2 - json object must have "model"')
return 0}
if(!typeof(json0.brand)=='string'){alert('updatemodel2 - json object must have "brand"')
return 0}
var form=$(json0.form)
if(!form.length){alert('updatemodel2 - '+json0.form+' not found')
return 0}
var model_select=form.find(json0.model)
if(model_select.length<1){alert('updatemodel2 - '+json0.model+' not found')
return 0}
var model_options=model_select.find('option[name]')
if(!model_options.length){alert('updatemodel2 - options must have name attributes to represent foreign key value in '+json0.model)
return 0}
var brand_select=form.find(json0.brand)
if(brand_select.length<1){alert('updatemodel2 - cannot find brand '+json0.brand)
return 0}
fake_select=$('<select id="fake_select"></select>').appendTo('body').hide()
var last_model_options=null;var selected_option=model_options.filter('option:selected')
if(selected_option.length>0){brand_select.val(selected_option.attr('name'))
model_options.filter('[name!='+brand_select.val()+']').appendTo(fake_select)
last_model_options=model_select.find('option[name]')}
else if(brand_select.val()){model_options.filter('[name!='+brand_select.val()+']').appendTo(fake_select)
last_model_options=model_select.find('option[name]')}
else{model_select.attr('disabled',true)
model_options.appendTo(fake_select)}
brand_select.change(function(e){var brand_option_val=$(this).val()
if(brand_option_val){model_select.removeAttr('disabled')
if(last_model_options&&last_model_options.length){last_model_options.appendTo(fake_select)}
last_model_options=model_options.filter('[name='+brand_option_val+']')
last_model_options.appendTo(model_select)
model_select.val('')}
else{model_select.attr('disabled',true)}})}
function updateModel3(json0){if(!typeof(json0)=='object'){alert('updatemodel2 - 1st argument must a json object')
return 0}
if(!typeof(json0.form)=='string'){alert('updatemodel2 - json object must have "form"')
return 0}
if(!typeof(json0.model)=='string'){alert('updatemodel2 - json object must have "model"')
return 0}
if(!typeof(json0.brand)=='string'){alert('updatemodel2 - json object must have "brand"')
return 0}
var form=$(json0.form)
if(!form.length){alert('updatemodel2 - '+json0.form+' not found')
return 0}
var model_select=form.find(json0.model)
if(model_select.length<1){alert('updatemodel2 - '+json0.model+' not found')
return 0}
var model_options=model_select.find('option[name]')
if(!model_options.length){alert('updatemodel2 - options must have name attributes to represent foreign key value in '+json0.model)
return 0}
var brand_select=form.find(json0.brand)
if(brand_select.length<1){alert('updatemodel2 - cannot find brand '+json0.brand)
return 0}
fake_select=$('<select id="fake_select"></select>').appendTo('body').hide()
var last_model_options=null;var selected_option=model_options.filter('option:selected')
if(selected_option.length>0){brand_select.val(selected_option.attr('name'))
model_options.filter('[name!='+brand_select.val()+']').appendTo(fake_select)
last_model_options=model_select.find('option[name]')}
else if(brand_select.val()){model_options.filter('[name!='+brand_select.val()+']').appendTo(fake_select)
last_model_options=model_select.find('option[name]')}
else{model_select.attr('disabled',true)
model_options.appendTo(fake_select)}
brand_select.change(function(e){var brand_option_val=$(this).val()
if(brand_option_val){model_select.removeAttr('disabled')
if(last_model_options&&last_model_options.length){last_model_options.appendTo(fake_select)}
temp_data=fake_select
last_model_options=model_options.filter('[name='+brand_option_val+']')
last_model_options.each(function(e){data=model_select.filter(':contains('+$(this).html()+')')
if(!data.length){$(this).appendTo(model_select)}})
model_select.val('')}
else{model_select.attr('disabled',true)}})}
function index_js(){$('#id_user_email').attr('size','60')
var div_warning=$('<div align="center" id="pop_up_msg" style="overflow: hidden; width: 100%; font-size: 20px; height: 30px;color:red;">Please wait while we processing your request.</div>')
$('.log_in2').click(function(e){if($("#id_user_email").val()!="")
{$(this).hide();$('<img src="/media/img/preloader-small.gif" style="margin-top:5px;"/>').insertAfter($(this))
$("#email_parent").append(div_warning)}})
$('#pop_up_ad').click(function(){$('#pop_up_ad').hide()})
$('#size_pop_up').hide()
$('#size_guide').click(function(e){e.preventDefault()
$('#size_pop_up').show()})
$('#close_size').click(function(e){e.preventDefault()
$('#size_pop_up').hide()})
$('#submit_ideal').click(function(e){e.preventDefault()
var feet=$('#ibw_height_feet')
var weight=$('#ibw_weight')
var heightFeet=parseInt(feet.val());var weight_val=parseInt(weight.val());var frame=$('.frame')
var frame_val;var data=false
var idealWeight=0.9*heightFeet-88;$('.frame').each(function(e){if($(this).attr('checked')){data=true;frame_val=$(this).val()}})
if(feet.val()==''){alert('Please fill your height.')
feet.focus()
feet.attr('style','background-color:red;')}
else if(weight.val()==''){alert('Please fill your weight')
weight.focus()
weight.attr('style','background-color:red;')}
else if(data==false){alert('Please choose your frame size')}
else{if(frame_val==1){frameSize="Small";idealWeight=parseInt(idealWeight)-10;}
if(frame_val==2){frameSize="Medium";}
if(frame_val==3){frameSize="Large";idealWeight=parseInt(idealWeight)+10;}
var maxIdealWeight=Math.round((parseInt(idealWeight)*1.1)*100)/100;var overWeightBy=Math.round((weight_val-parseFloat(maxIdealWeight))*100)/100;var difference=parseFloat(overWeightBy)+' lbs. ('+Math.round(((overWeightBy)*100)/100)+' kg.).';var weightRange=Math.round((idealWeight)*10)/10+' - '+Math.round((maxIdealWeight)*100)/100+' kg.';idealWeight=weight_val/idealWeight;idealWeight=Math.round(idealWeight*100)/100;if((idealWeight>=1.00)&&(idealWeight<=1.10))
IBWCalculation="Contratulations! Your weight is ideal!";else if((idealWeight>1.10)&&(idealWeight<1.20))
IBWCalculation="You are marginally overweight by "+difference;else if((idealWeight>=1.20)&&(idealWeight<=1.30))
IBWCalculation="You are overweight by "+difference;else if(idealWeight>1.30)
IBWCalculation="You are overweight by "+difference+"<br>You may wish to consult with your physician for medical help.";else
IBWCalculation="You are underweight.";IBWCalculation='<div style="overflow:hidden;height:145px;" id="ideal_res">'+"Ideal weight range is "+weightRange+'<br>'+IBWCalculation+'<br> --is based on a formula that calculates what a healthy weight is for most people of your height ('+heightFeet+') and frame size ('+frameSize+').'+'</div><div><a href="#" id="back_ideal" class="short_red_button">back</a></div>';$('#ideal_res').html(IBWCalculation)
$('#ideal_res').show()
$('#ideal_form').hide()}
$('#back_ideal').click(function(e){e.preventDefault()
$('#ideal_res').hide()
$('#ideal_form').show()
$('#back_ideal').attr('style','display:none;')})})
if(click_value==1){$('#view').addClass('selected')}
else if(click_value==2)
{$('#comment').addClass('selected')
$('#view').removeClass('selected')}
else if(click_value==3)
{$('#favorite').addClass('selected')
$('#view').removeClass('selected')}
else if(click_value==4)
{$('#updated').addClass('selected')
$('#view').removeClass('selected')}
else
{$('#invite').addClass('selected')
$('#view').removeClass('selected')}
$('#row_pic1').animate({top:"0px"},300)
$('#row_pic2').animate({top:"0px"},300)
$('#row_pic3').animate({top:"0px"},300)
$('#row_pic4').animate({top:"0px"},300)
if(!$.mobile()){var a=$(".initial").val()
hiConfig={sensitivity:7,interval:150,timeout:100,over:function(){$('#row_pic2').animate({top:"0px"},300)
$('#row_pic3').animate({top:"0px"},300)
$('#row_pic4').animate({top:"0px"},300)
if(a!=1){var get_flash_url=$("#row_pic1 input").val()
var MEDIA_URL="/media/"
var src_flash_picture=MEDIA_URL+get_flash_url
$('.flash_picture').animate({"height":"toggle","opacity":"toggle"},{"duration":"fast"})
$('.flash_picture').animate({"height":"toggle","opacity":"toggle"},{"duration":"slow"}).attr('src',src_flash_picture)
$('#row_pic1').animate({top:"-30px"},300)
a=1}},out:function(){if(a!=1){var get_flash_url=$("#row_pic1 input").val()
var MEDIA_URL="/media/"
var src_flash_picture=MEDIA_URL+get_flash_url
$('#row_pic1').animate({top:"-30px"},300)}}}
$('#row_pic1').hoverIntent(hiConfig)
hiConfig={sensitivity:7,interval:150,timeout:100,over:function(){$('#row_pic1').animate({top:"0px"},300)
$('#row_pic3').animate({top:"0px"},300)
$('#row_pic4').animate({top:"0px"},300)
if(a!=2){$('.flash_picture').animate({"height":"toggle","opacity":"toggle"},{"duration":"fast"})
var get_flash_url=$("#row_pic2 input").val()
var MEDIA_URL="/media/"
var src_flash_picture=MEDIA_URL+get_flash_url
$('.flash_picture').animate({"height":"toggle","opacity":"toggle"},{"duration":"slow"}).attr('src',src_flash_picture)
$('#row_pic2').animate({top:"-30px"},300)
a=2}},out:function(){if(a!=2){var get_flash_url=$("#row_pic2 input").val()
var MEDIA_URL="/media/"
var src_flash_picture=MEDIA_URL+get_flash_url
$('#row_pic2').animate({top:"-30px"},300)}}}
$('#row_pic2').hoverIntent(hiConfig)
hiConfig={sensitivity:7,interval:150,timeout:100,over:function(){$('#row_pic2').animate({top:"0px"},300)
$('#row_pic1').animate({top:"0px"},300)
$('#row_pic4').animate({top:"0px"},300)
if(a!=3){$('.flash_picture').animate({"height":"toggle","opacity":"toggle"},{"duration":"fast"})
var get_flash_url=$("#row_pic3 input").val()
var MEDIA_URL="/media/"
var src_flash_picture=MEDIA_URL+get_flash_url
$('.flash_picture').animate({"height":"toggle","opacity":"toggle"},{"duration":"slow"}).attr('src',src_flash_picture)
$('#row_pic3').animate({top:"-30px"},300)
a=3}},out:function(){if(a!=3){var get_flash_url=$("#row_pic3 input").val()
var MEDIA_URL="/media/"
var src_flash_picture=MEDIA_URL+get_flash_url
$('#row_pic3').animate({top:"-30px"},300)}}}
$('#row_pic3').hoverIntent(hiConfig)
hiConfig={sensitivity:7,interval:150,timeout:100,over:function(){$('#row_pic2').animate({top:"0px"},300)
$('#row_pic3').animate({top:"0px"},300)
$('#row_pic1').animate({top:"0px"},300)
if(a!=4){$('.flash_picture').animate({"height":"toggle","opacity":"toggle"},{"duration":"fast"})
var get_flash_url=$("#row_pic4 input").val()
var MEDIA_URL="/media/"
var src_flash_picture=MEDIA_URL+get_flash_url
$('.flash_picture').animate({"height":"toggle","opacity":"toggle"},{"duration":"slow"}).attr('src',src_flash_picture)
$('#row_pic4').animate({top:"-30px"},300)
a=4}},out:function(){if(a!=4){var get_flash_url=$("#row_pic4 input").val()
var MEDIA_URL="/media/"
var src_flash_picture=MEDIA_URL+get_flash_url
$('#row_pic4').animate({top:"-30px"},300)}}}
$('#row_pic4').hoverIntent(hiConfig)}}
function acc_base_js(){$('#dropdown2').hide()
$(".sf-menu").superfish({animation:{height:'show'},delay:2000});$('#all_col').click(function(e){e.preventDefault()})
if(window.attachEvent)window.attachEvent("onload",sfHover);$('#clickme').cluetip({activation:'click',sticky:true,closePosition:'title',width:350,splitTitle:'|'});$('#side_add_collection_clickme').cluetip({activation:'click',sticky:true,closePosition:'title',width:350,splitTitle:'|'});}
function detail_items_js(){$('#addict_clickme').cluetip({activation:'click',sticky:true,closePosition:'title',width:350,splitTitle:'|'});$('#compare_clickme').cluetip({activation:'click',sticky:true,closePosition:'title',width:350,splitTitle:'|'});$('#id_comment').css('width','372px')
$('#id_comment').css('height','100px')
$('#bottom_ad').hide();var id=$('#item_id').val()
$('#change_img').attr('style','cursor:pointer');$('#change_img1').attr('style','cursor:pointer');all.show();if('{{item.line.store.user.id}}'=='{{user.id}}'){img.attr('style','display:;border:none;');name1.attr('style',' color:#B5121C; font-weight:bold; margin-left:0px')
img.attr('src','/media/fashion_icon.png');}
if(id==id_line_items1){$('#item1 .rows').show()}
if(id==id_line_items2){$('#item2 .rows').show()}
if(id==id_line_items3){$('#item3 .rows').show()}
if(id==id_line_items4){$('#item4 .rows').show()}
if(id==id_line_items5){$('#item5 .rows').show()}
$('#product_picture').click(function(e){e.preventDefault()
$('#detail_picture').removeAttr('style')
$('#detail_picture').attr('style','display:block;position:absolute;top:295px;z-index:2000;background-color:white;height:500px;')})
$('.close').click(function(e){e.preventDefault()
$('#detail_picture').attr('style','display:none')})
$('#example-1').ratings(5).bind('ratingchanged',function(event,data){$('#example-rating-1').text(data.rating);});$('#form1').submitLoad()}
function compare_thumb_js(){if(!$.mobile()){store1.click(function(){all1.hide();unhide.attr('src','');name2.attr('style',' color:#B5121C; font-weight:bold;')})
unhide.attr('style','display:;border:none;');all1.show();unhide.attr('src','/media/fashion_icon.png');name2.attr('style',' color:#B5121C; font-weight:bold;')
$('.star_counter_class').each(function(i){var stars=$([])
var input_value=$(this).val()
if(input_value!=0){for(var i=0;i<input_value;i++){$('<img src="/media/full-star.png" />').insertBefore($(this))}
if(input_value!=5)
{for(var a=input_value;a<5;a++){$('<img src="/media/empty-star.png" />').insertBefore($(this))}}}
else{for(var a=input_value;a<5;a++){$('<img src="/media/empty-star.png" />').insertBefore($(this))}}})
$('#uncheck_all').click(function(e){e.preventDefault()
$('.input').attr('checked',false)})}}
function view_detail_compare_js(){if(!$.mobile()){unhide.attr('style','display:;border:none;');all1.show();unhide.attr('src','/media/fashion_icon.png');name2.attr('style',' color:#B5121C; font-weight:bold;')
$('.horoscopePanel').hide();$('.horoscopePanel1').hide();$('.description a').click(function(e){e.preventDefault()})
$('.location a').click(function(e){e.preventDefault()})
$('.side_menu_box').attr('style','height:860px;')
$('.star_counter_class').each(function(i){var stars=$([])
var input_value=$(this).val()
if(input_value!=0){for(var i=0;i<input_value;i++){$('<img src="/media/full-star.png" />').insertBefore($(this))}
if(input_value!=5)
{for(var a=input_value;a<5;a++){$('<img src="/media/empty-star.png" />').insertBefore($(this))}}}
else{for(var a=input_value;a<5;a++){$('<img src="/media/empty-star.png" />').insertBefore($(this))}}})
var new_location1=$('.location a').each(function(i){$(this).click(function(a){$('.horoscopePanel1').each(function(d){$(this).hide();var test1=$(this).html()
$(this).html(test1);$('.close1').click(function(e){e.preventDefault();$(this).parent().parent().hide();})})
$(this).next('.horoscopePanel1').toggle()})})
var new_location=$('.description a').each(function(i){$(".cross1").each(function(f){$(this).attr('src','/media/cross.png');});$(this).click(function(a){$('.horoscopePanel').each(function(e){$(this).hide();var test=$(this).html()
$(this).html(test);$('.x_close').click(function(e){e.preventDefault();$(this).parents('.horoscopePanel').hide();})})
$(this).next().toggle()})})}}
function notification_js(){if(!$.mobile()){$('#store1').click(function(){all2.hide();expand.attr('src','');name3.attr('style',' color:#B5121C;font-weight:bold; margin-left:20px')})
$('#id_select').change(function(e){$('#form1').submit();})
expand.attr('style','display:inline;border:none;');all2.show();expand.attr('src','/media/fashion_icon.png');name3.attr('style',' color:#B5121C; font-weight:bold; margin-left:0px')
$("input[name=topics]").click(function(){var length=$(this).length
if($("input[name=topics]").length!=$("input[name=topics]:checked").length){$(".checkall").each(function()
{$(this).attr('checked',false)});}});$('.checkall').click(function(){var checked_status=this.checked;$(".checkall").each(function(){this.checked=checked_status;});$("input[name=topics]").each(function()
{this.checked=checked_status;});})}}
function send_items_js(){store1.click(function(){all2.hide();expand.attr('src','');name3.attr('style',' color:#B5121C;font-weight:bold; margin-left:20px')})
if(!$.mobile()){$('#id_select').change(function(e){$('#form1').submit();})
expand.attr('style','display:;border:none;');all2.show();expand.attr('src','/media/fashion_icon.png');name3.attr('style',' color:#B5121C; font-weight:bold; margin-left:0px')
$("input[name=topics]").click(function(){var length=$(this).length
if($("input[name=topics]").length!=$("input[name=topics]:checked").length){$(".checkall").each(function()
{$(this).attr('checked',false)});}});$('.checkall').click(function(){var checked_status=this.checked;$(".checkall").each(function(){this.checked=checked_status;});$("input[name=topics]").each(function()
{this.checked=checked_status;});})}}
function edit_profile_js(){if($('#id_country').val()!="1"){$('#id_province').attr('disabled',true);}
var prof_img=$('#profile_img')
var prof=$('#name7')
prof_img.attr('style','display:;border:none;');prof_img.attr('src','{{MEDIA_URL}}fashion_icon.png');prof.attr('style',' color:#B5121C; font-weight:bold;')
updateModel2({form:'#edit_form',model:'#id_province',brand:'#id_country'})
updateModel2({form:'#edit_form',model:'#id_phone_area_code',brand:'#id_province'})
updateModel2({form:'#edit_form',model:'#id_fax_area_code',brand:'#id_province'})
$('#column9').hide()
$('#id_phone_area_code').insertAfter($('#columnb10'))
$('#column12').hide()
$('#id_fax_area_code').insertAfter($('#columnb13'))
$("#id_date_of_birth").datepicker({showAnim:'slideDown',altField:'#id_date_of_birth',altFormat:'dd/mm/yy',changeMonth:true,changeYear:true,minDate:new Date(1950,0,1),maxDate:new Date(2000,12,0),yearRange:'1950:2000',defaultDate:new Date(1950,0,1),showOn:'button',buttonImage:'{{ MEDIA_URL}}css/images/calendar.gif',buttonImageOnly:true});$('.side_menu_box').css('height','1010px')
$('#column18').attr('style','width:300px;')
$('#id_date_of_birth').attr('readonly',true)
$('#id_telephone').numeric({allow:"+"});$('#id_post_code').numeric();$('#id_handphone').numeric({allow:"+"});$('#id_fax').numeric({allow:"+"});$('#id_country').change(function(){if($(this).val()=="1"){$('#id_phone_area_code').attr('disabled',false);$('#id_fax_area_code').attr('disabled',false);}else{$('#id_province').attr('disabled',true);$('#id_phone_area_code').attr('disabled',true);$('#id_fax_area_code').attr('disabled',true);}})
fieldlimiter.setup({thefield:document.getElementById("id_street_address"),maxlength:100,statusids:["eg5"],onkeypress:function(maxlength,curlength){}})
fieldlimiter.setup({thefield:document.getElementById("id_about_me"),maxlength:1000,statusids:["eg16"],onkeypress:function(maxlength,curlength){}})};(function($){$.fn.extend({autocomplete:function(urlOrData,options){var isUrl=typeof urlOrData=="string";options=$.extend({},$.Autocompleter.defaults,{url:isUrl?urlOrData:null,data:isUrl?null:urlOrData,delay:isUrl?$.Autocompleter.defaults.delay:10,max:options&&!options.scroll?10:150},options);options.highlight=options.highlight||function(value){return value;};options.formatMatch=options.formatMatch||options.formatItem;return this.each(function(){new $.Autocompleter(this,options);});},result:function(handler){return this.bind("result",handler);},search:function(handler){return this.trigger("search",[handler]);},flushCache:function(){return this.trigger("flushCache");},setOptions:function(options){return this.trigger("setOptions",[options]);},unautocomplete:function(){return this.trigger("unautocomplete");}});$.Autocompleter=function(input,options){var KEY={UP:38,DOWN:40,DEL:46,TAB:9,RETURN:13,ESC:27,COMMA:188,PAGEUP:33,PAGEDOWN:34,BACKSPACE:8};var $input=$(input).attr("autocomplete","off").addClass(options.inputClass);var timeout;var previousValue="";var cache=$.Autocompleter.Cache(options);var hasFocus=0;var lastKeyPressCode;var config={mouseDownOnSelect:false};var select=$.Autocompleter.Select(options,input,selectCurrent,config);var blockSubmit;$.browser.opera&&$(input.form).bind("submit.autocomplete",function(){if(blockSubmit){blockSubmit=false;return false;}});$input.bind(($.browser.opera?"keypress":"keydown")+".autocomplete",function(event){hasFocus=1;lastKeyPressCode=event.keyCode;switch(event.keyCode){case KEY.UP:event.preventDefault();if(select.visible()){select.prev();}else{onChange(0,true);}
break;case KEY.DOWN:event.preventDefault();if(select.visible()){select.next();}else{onChange(0,true);}
break;case KEY.PAGEUP:event.preventDefault();if(select.visible()){select.pageUp();}else{onChange(0,true);}
break;case KEY.PAGEDOWN:event.preventDefault();if(select.visible()){select.pageDown();}else{onChange(0,true);}
break;case options.multiple&&$.trim(options.multipleSeparator)==","&&KEY.COMMA:case KEY.TAB:case KEY.RETURN:if(selectCurrent()){event.preventDefault();blockSubmit=true;return false;}
break;case KEY.ESC:select.hide();break;default:clearTimeout(timeout);timeout=setTimeout(onChange,options.delay);break;}}).focus(function(){hasFocus++;}).blur(function(){hasFocus=0;if(!config.mouseDownOnSelect){hideResults();}}).click(function(){if(hasFocus++>1&&!select.visible()){onChange(0,true);}}).bind("search",function(){var fn=(arguments.length>1)?arguments[1]:null;function findValueCallback(q,data){var result;if(data&&data.length){for(var i=0;i<data.length;i++){if(data[i].result.toLowerCase()==q.toLowerCase()){result=data[i];break;}}}
if(typeof fn=="function")fn(result);else $input.trigger("result",result&&[result.data,result.value]);}
$.each(trimWords($input.val()),function(i,value){request(value,findValueCallback,findValueCallback);});}).bind("flushCache",function(){cache.flush();}).bind("setOptions",function(){$.extend(options,arguments[1]);if("data"in arguments[1])
cache.populate();}).bind("unautocomplete",function(){select.unbind();$input.unbind();$(input.form).unbind(".autocomplete");});function selectCurrent(){var selected=select.selected();if(!selected)
return false;var v=selected.result;previousValue=v;if(options.multiple){var words=trimWords($input.val());if(words.length>1){var seperator=options.multipleSeparator.length;var cursorAt=$(input).selection().start;var wordAt,progress=0;$.each(words,function(i,word){progress+=word.length;if(cursorAt<=progress){wordAt=i;return false;}
progress+=seperator;});words[wordAt]=v;v=words.join(options.multipleSeparator);}
v+=options.multipleSeparator;}
$input.val(v);hideResultsNow();$input.trigger("result",[selected.data,selected.value]);return true;}
function onChange(crap,skipPrevCheck){if(lastKeyPressCode==KEY.DEL){select.hide();return;}
var currentValue=$input.val();if(!skipPrevCheck&&currentValue==previousValue)
return;previousValue=currentValue;currentValue=lastWord(currentValue);if(currentValue.length>=options.minChars){$input.addClass(options.loadingClass);if(!options.matchCase)
currentValue=currentValue.toLowerCase();request(currentValue,receiveData,hideResultsNow);}else{stopLoading();select.hide();}};function trimWords(value){if(!value)
return[""];if(!options.multiple)
return[$.trim(value)];return $.map(value.split(options.multipleSeparator),function(word){return $.trim(value).length?$.trim(word):null;});}
function lastWord(value){if(!options.multiple)
return value;var words=trimWords(value);if(words.length==1)
return words[0];var cursorAt=$(input).selection().start;if(cursorAt==value.length){words=trimWords(value)}else{words=trimWords(value.replace(value.substring(cursorAt),""));}
return words[words.length-1];}
function autoFill(q,sValue){if(options.autoFill&&(lastWord($input.val()).toLowerCase()==q.toLowerCase())&&lastKeyPressCode!=KEY.BACKSPACE){$input.val($input.val()+sValue.substring(lastWord(previousValue).length));$(input).selection(previousValue.length,previousValue.length+sValue.length);}};function hideResults(){clearTimeout(timeout);timeout=setTimeout(hideResultsNow,200);};function hideResultsNow(){var wasVisible=select.visible();select.hide();clearTimeout(timeout);stopLoading();if(options.mustMatch){$input.search(function(result){if(!result){if(options.multiple){var words=trimWords($input.val()).slice(0,-1);$input.val(words.join(options.multipleSeparator)+(words.length?options.multipleSeparator:""));}
else{$input.val("");$input.trigger("result",null);}}});}};function receiveData(q,data){if(data&&data.length&&hasFocus){stopLoading();select.display(data,q);autoFill(q,data[0].value);select.show();}else{hideResultsNow();}};function request(term,success,failure){if(!options.matchCase)
term=term.toLowerCase();var data=cache.load(term);if(data&&data.length){success(term,data);}else if((typeof options.url=="string")&&(options.url.length>0)){var extraParams={timestamp:+new Date()};$.each(options.extraParams,function(key,param){extraParams[key]=typeof param=="function"?param():param;});$.ajax({mode:"abort",port:"autocomplete"+input.name,dataType:options.dataType,url:options.url,data:$.extend({q:lastWord(term),limit:options.max},extraParams),success:function(data){var parsed=options.parse&&options.parse(data)||parse(data);cache.add(term,parsed);success(term,parsed);}});}else{select.emptyList();failure(term);}};function parse(data){var parsed=[];var rows=data.split("\n");for(var i=0;i<rows.length;i++){var row=$.trim(rows[i]);if(row){row=row.split("|");parsed[parsed.length]={data:row,value:row[0],result:options.formatResult&&options.formatResult(row,row[0])||row[0]};}}
return parsed;};function stopLoading(){$input.removeClass(options.loadingClass);};};$.Autocompleter.defaults={inputClass:"ac_input",resultsClass:"ac_results",loadingClass:"ac_loading",minChars:1,delay:400,matchCase:false,matchSubset:true,matchContains:false,cacheLength:10,max:100,mustMatch:false,extraParams:{},selectFirst:true,formatItem:function(row){return row[0];},formatMatch:null,autoFill:false,width:0,multiple:false,multipleSeparator:", ",highlight:function(value,term){return value.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)("+term.replace(/([\^\$\(\)\[\]\{\}\*\.\+\?\|\\])/gi,"\\$1")+")(?![^<>]*>)(?![^&;]+;)","gi"),"<strong>$1</strong>");},scroll:true,scrollHeight:180};$.Autocompleter.Cache=function(options){var data={};var length=0;function matchSubset(s,sub){if(!options.matchCase)
s=s.toLowerCase();var i=s.indexOf(sub);if(options.matchContains=="word"){i=s.toLowerCase().search("\\b"+sub.toLowerCase());}
if(i==-1)return false;return i==0||options.matchContains;};function add(q,value){if(length>options.cacheLength){flush();}
if(!data[q]){length++;}
data[q]=value;}
function populate(){if(!options.data)return false;var stMatchSets={},nullData=0;if(!options.url)options.cacheLength=1;stMatchSets[""]=[];for(var i=0,ol=options.data.length;i<ol;i++){var rawValue=options.data[i];rawValue=(typeof rawValue=="string")?[rawValue]:rawValue;var value=options.formatMatch(rawValue,i+1,options.data.length);if(value===false)
continue;var firstChar=value.charAt(0).toLowerCase();if(!stMatchSets[firstChar])
stMatchSets[firstChar]=[];var row={value:value,data:rawValue,result:options.formatResult&&options.formatResult(rawValue)||value};stMatchSets[firstChar].push(row);if(nullData++<options.max){stMatchSets[""].push(row);}};$.each(stMatchSets,function(i,value){options.cacheLength++;add(i,value);});}
setTimeout(populate,25);function flush(){data={};length=0;}
return{flush:flush,add:add,populate:populate,load:function(q){if(!options.cacheLength||!length)
return null;if(!options.url&&options.matchContains){var csub=[];for(var k in data){if(k.length>0){var c=data[k];$.each(c,function(i,x){if(matchSubset(x.value,q)){csub.push(x);}});}}
return csub;}else
if(data[q]){return data[q];}else
if(options.matchSubset){for(var i=q.length-1;i>=options.minChars;i--){var c=data[q.substr(0,i)];if(c){var csub=[];$.each(c,function(i,x){if(matchSubset(x.value,q)){csub[csub.length]=x;}});return csub;}}}
return null;}};};$.Autocompleter.Select=function(options,input,select,config){var CLASSES={ACTIVE:"ac_over"};var listItems,active=-1,data,term="",needsInit=true,element,list;function init(){if(!needsInit)
return;element=$("<div/>").hide().addClass(options.resultsClass).css("position","absolute").appendTo(document.body);list=$("<ul/>").appendTo(element).mouseover(function(event){if(target(event).nodeName&&target(event).nodeName.toUpperCase()=='LI'){active=$("li",list).removeClass(CLASSES.ACTIVE).index(target(event));$(target(event)).addClass(CLASSES.ACTIVE);}}).click(function(event){$(target(event)).addClass(CLASSES.ACTIVE);select();input.focus();return false;}).mousedown(function(){config.mouseDownOnSelect=true;}).mouseup(function(){config.mouseDownOnSelect=false;});if(options.width>0)
element.css("width",options.width);needsInit=false;}
function target(event){var element=event.target;while(element&&element.tagName!="LI")
element=element.parentNode;if(!element)
return[];return element;}
function moveSelect(step){listItems.slice(active,active+1).removeClass(CLASSES.ACTIVE);movePosition(step);var activeItem=listItems.slice(active,active+1).addClass(CLASSES.ACTIVE);if(options.scroll){var offset=0;listItems.slice(0,active).each(function(){offset+=this.offsetHeight;});if((offset+activeItem[0].offsetHeight-list.scrollTop())>list[0].clientHeight){list.scrollTop(offset+activeItem[0].offsetHeight-list.innerHeight());}else if(offset<list.scrollTop()){list.scrollTop(offset);}}};function movePosition(step){active+=step;if(active<0){active=listItems.size()-1;}else if(active>=listItems.size()){active=0;}}
function limitNumberOfItems(available){return options.max&&options.max<available?options.max:available;}
function fillList(){list.empty();var max=limitNumberOfItems(data.length);for(var i=0;i<max;i++){if(!data[i])
continue;var formatted=options.formatItem(data[i].data,i+1,max,data[i].value,term);if(formatted===false)
continue;var li=$("<li/>").html(options.highlight(formatted,term)).addClass(i%2==0?"ac_even":"ac_odd").appendTo(list)[0];$.data(li,"ac_data",data[i]);}
listItems=list.find("li");if(options.selectFirst){listItems.slice(0,1).addClass(CLASSES.ACTIVE);active=0;}
if($.fn.bgiframe)
list.bgiframe();}
return{display:function(d,q){init();data=d;term=q;fillList();},next:function(){moveSelect(1);},prev:function(){moveSelect(-1);},pageUp:function(){if(active!=0&&active-8<0){moveSelect(-active);}else{moveSelect(-8);}},pageDown:function(){if(active!=listItems.size()-1&&active+8>listItems.size()){moveSelect(listItems.size()-1-active);}else{moveSelect(8);}},hide:function(){element&&element.hide();listItems&&listItems.removeClass(CLASSES.ACTIVE);active=-1;},visible:function(){return element&&element.is(":visible");},current:function(){return this.visible()&&(listItems.filter("."+CLASSES.ACTIVE)[0]||options.selectFirst&&listItems[0]);},show:function(){var offset=$(input).offset();element.css({width:typeof options.width=="string"||options.width>0?options.width:$(input).width(),top:offset.top+input.offsetHeight,left:offset.left}).show();if(options.scroll){list.scrollTop(0);list.css({maxHeight:options.scrollHeight,overflow:'auto'});if($.browser.msie&&typeof document.body.style.maxHeight==="undefined"){var listHeight=0;listItems.each(function(){listHeight+=this.offsetHeight;});var scrollbarsVisible=listHeight>options.scrollHeight;list.css('height',scrollbarsVisible?options.scrollHeight:listHeight);if(!scrollbarsVisible){listItems.width(list.width()-parseInt(listItems.css("padding-left"))-parseInt(listItems.css("padding-right")));}}}},selected:function(){var selected=listItems&&listItems.filter("."+CLASSES.ACTIVE).removeClass(CLASSES.ACTIVE);return selected&&selected.length&&$.data(selected[0],"ac_data");},emptyList:function(){list&&list.empty();},unbind:function(){element&&element.remove();}};};$.fn.selection=function(start,end){if(start!==undefined){return this.each(function(){if(this.createTextRange){var selRange=this.createTextRange();if(end===undefined||start==end){selRange.move("character",start);selRange.select();}else{selRange.collapse(true);selRange.moveStart("character",start);selRange.moveEnd("character",end);selRange.select();}}else if(this.setSelectionRange){this.setSelectionRange(start,end);}else if(this.selectionStart){this.selectionStart=start;this.selectionEnd=end;}});}
var field=this[0];if(field.createTextRange){var range=document.selection.createRange(),orig=field.value,teststring="<->",textLength=range.text.length;range.text=teststring;var caretAt=field.value.indexOf(teststring);field.value=orig;this.selection(caretAt,caretAt+textLength);return{start:caretAt,end:caretAt+textLength}}else if(field.selectionStart!==undefined){return{start:field.selectionStart,end:field.selectionEnd}}};})(jQuery);;(function($){$.cluetip={version:'1.0.3'};var $cluetip,$cluetipInner,$cluetipOuter,$cluetipTitle,$cluetipArrows,$cluetipWait,$dropShadow,imgCount;$.fn.cluetip=function(js,options){if(typeof js=='object'){options=js;js=null;}
if(js=='destroy'){return this.unbind('.cluetip');}
return this.each(function(index){var link=this,$this=$(this);var opts=$.extend(true,{},$.fn.cluetip.defaults,options||{},$.metadata?$this.metadata():$.meta?$this.data():{});var cluetipContents=false;var cluezIndex=+opts.cluezIndex;$this.data('thisInfo',{title:link.title,zIndex:cluezIndex});var isActive=false,closeOnDelay=0;if(!$('#cluetip').length){$(['<div id="cluetip">','<div id="cluetip-outer">','<h3 id="cluetip-title"></h3>','<div id="cluetip-inner"></div>','</div>','<div id="cluetip-extra"></div>','<div id="cluetip-arrows" class="cluetip-arrows"></div>','</div>'].join(''))
[insertionType](insertionElement).hide();$cluetip=$('#cluetip').css({position:'absolute'});$cluetipOuter=$('#cluetip-outer').css({position:'relative',zIndex:cluezIndex});$cluetipInner=$('#cluetip-inner');$cluetipTitle=$('#cluetip-title');$cluetipArrows=$('#cluetip-arrows');$cluetipWait=$('<div id="cluetip-waitimage"></div>').css({position:'absolute'}).insertBefore($cluetip).hide();}
var dropShadowSteps=(opts.dropShadow)?+opts.dropShadowSteps:0;if(!$dropShadow){$dropShadow=$([]);for(var i=0;i<dropShadowSteps;i++){$dropShadow=$dropShadow.add($('<div></div>').css({zIndex:cluezIndex-1,opacity:.1,top:1+i,left:1+i}));};$dropShadow.css({position:'absolute',backgroundColor:'#000'}).prependTo($cluetip);}
var tipAttribute=$this.attr(opts.attribute),ctClass=opts.cluetipClass;if(!tipAttribute&&!opts.splitTitle&&!js)return true;if(opts.local&&opts.localPrefix){tipAttribute=opts.localPrefix+tipAttribute;}
if(opts.local&&opts.hideLocal){$(tipAttribute+':first').hide();}
var tOffset=parseInt(opts.topOffset,10),lOffset=parseInt(opts.leftOffset,10);var tipHeight,wHeight,defHeight=isNaN(parseInt(opts.height,10))?'auto':(/\D/g).test(opts.height)?opts.height:opts.height+'px';var sTop,linkTop,posY,tipY,mouseY,baseline;var tipInnerWidth=parseInt(opts.width,10)||275,tipWidth=tipInnerWidth+(parseInt($cluetip.css('paddingLeft'),10)||0)+(parseInt($cluetip.css('paddingRight'),10)||0)+dropShadowSteps,linkWidth=this.offsetWidth,linkLeft,posX,tipX,mouseX,winWidth;var tipParts;var tipTitle=(opts.attribute!='title')?$this.attr(opts.titleAttribute):'';if(opts.splitTitle){if(tipTitle==undefined){tipTitle='';}
tipParts=tipTitle.split(opts.splitTitle);tipTitle=tipParts.shift();}
if(opts.escapeTitle){tipTitle=tipTitle.replace(/&/g,'&amp;').replace(/>/g,'&gt;').replace(/</g,'&lt;');}
var localContent;var activate=function(event){if(!opts.onActivate($this)){return false;}
isActive=true;$cluetip.removeClass().css({width:tipInnerWidth});if(tipAttribute==$this.attr('href')){$this.css('cursor',opts.cursor);}
if(opts.hoverClass){$this.addClass(opts.hoverClass);}
linkTop=posY=$this.offset().top;linkLeft=$this.offset().left;mouseX=event.pageX;mouseY=event.pageY;if(link.tagName.toLowerCase()!='area'){sTop=$(document).scrollTop();winWidth=$(window).width();}
if(opts.positionBy=='fixed'){posX=linkWidth+linkLeft+lOffset;$cluetip.css({left:posX});}else{posX=(linkWidth>linkLeft&&linkLeft>tipWidth)||linkLeft+linkWidth+tipWidth+lOffset>winWidth?linkLeft-tipWidth-lOffset:linkWidth+linkLeft+lOffset;if(link.tagName.toLowerCase()=='area'||opts.positionBy=='mouse'||linkWidth+tipWidth>winWidth){if(mouseX+20+tipWidth>winWidth){$cluetip.addClass(' cluetip-'+ctClass);posX=(mouseX-tipWidth-lOffset)>=0?mouseX-tipWidth-lOffset-parseInt($cluetip.css('marginLeft'),10)+parseInt($cluetipInner.css('marginRight'),10):mouseX-(tipWidth/2);}else{posX=mouseX+lOffset;}}
var pY=posX<0?event.pageY+tOffset:event.pageY;$cluetip.css({left:(posX>0&&opts.positionBy!='bottomTop')?posX:(mouseX+(tipWidth/2)>winWidth)?winWidth/2-tipWidth/2:Math.max(mouseX-(tipWidth/2),0),zIndex:$this.data('thisInfo').zIndex});$cluetipArrows.css({zIndex:$this.data('thisInfo').zIndex+1});}
wHeight=$(window).height();if(js){if(typeof js=='function'){js=js(link);}
$cluetipInner.html(js);cluetipShow(pY);}
else if(tipParts){var tpl=tipParts.length;$cluetipInner.html(tipParts[0]);if(tpl>1){for(var i=1;i<tpl;i++){$cluetipInner.append('<div class="split-body">'+tipParts[i]+'</div>');}}
cluetipShow(pY);}
else if(!opts.local&&tipAttribute.indexOf('#')!=0){if(/\.(jpe?g|tiff?|gif|png)$/i.test(tipAttribute)){$cluetipInner.html('<img src="'+tipAttribute+'" alt="'+tipTitle+'" />');cluetipShow(pY);}else if(cluetipContents&&opts.ajaxCache){$cluetipInner.html(cluetipContents);cluetipShow(pY);}else{var optionBeforeSend=opts.ajaxSettings.beforeSend,optionError=opts.ajaxSettings.error,optionSuccess=opts.ajaxSettings.success,optionComplete=opts.ajaxSettings.complete;var ajaxSettings={cache:false,url:tipAttribute,beforeSend:function(xhr){if(optionBeforeSend){optionBeforeSend.call(link,xhr,$cluetip,$cluetipInner);}
$cluetipOuter.children().empty();if(opts.waitImage){$cluetipWait.css({top:mouseY+20,left:mouseX+20,zIndex:$this.data('thisInfo').zIndex-1}).show();}},error:function(xhr,textStatus){if(isActive){if(optionError){optionError.call(link,xhr,textStatus,$cluetip,$cluetipInner);}else{$cluetipInner.html('<i>sorry, the contents could not be loaded</i>');}}},success:function(data,textStatus){cluetipContents=opts.ajaxProcess.call(link,data);if(isActive){if(optionSuccess){optionSuccess.call(link,data,textStatus,$cluetip,$cluetipInner);}
$cluetipInner.html(cluetipContents);}},complete:function(xhr,textStatus){if(optionComplete){optionComplete.call(link,xhr,textStatus,$cluetip,$cluetipInner);}
imgCount=$('#cluetip-inner img').length;if(imgCount&&!$.browser.opera){$('#cluetip-inner img').bind('load error',function(){imgCount--;if(imgCount<1){$cluetipWait.hide();if(isActive)cluetipShow(pY);}});}else{$cluetipWait.hide();if(isActive){cluetipShow(pY);}}}};var ajaxMergedSettings=$.extend(true,{},opts.ajaxSettings,ajaxSettings);$.ajax(ajaxMergedSettings);}}else if(opts.local){var $localContent=$(tipAttribute+(/#\S+$/.test(tipAttribute)?'':':eq('+index+')')).clone(true).show();$cluetipInner.html($localContent);cluetipShow(pY);}};var cluetipShow=function(bpY){$cluetip.addClass('cluetip-'+ctClass);if(opts.truncate){var $truncloaded=$cluetipInner.text().slice(0,opts.truncate)+'...';$cluetipInner.html($truncloaded);}
function doNothing(){};tipTitle?$cluetipTitle.show().html(tipTitle):(opts.showTitle)?$cluetipTitle.show().html('&nbsp;'):$cluetipTitle.hide();if(opts.sticky){var $closeLink=$('<div id="cluetip-close"><a href="#">'+opts.closeText+'</a></div>');(opts.closePosition=='bottom')?$closeLink.appendTo($cluetipInner):(opts.closePosition=='title')?$closeLink.prependTo($cluetipTitle):$closeLink.prependTo($cluetipInner);$closeLink.bind('click.cluetip',function(){cluetipClose();return false;});if(opts.mouseOutClose){if($.fn.hoverIntent&&opts.hoverIntent){$cluetip.hoverIntent({over:doNothing,timeout:opts.hoverIntent.timeout,out:function(){$closeLink.trigger('click.cluetip');}});}else{$cluetip.hover(doNothing,function(){$closeLink.trigger('click.cluetip');});}}else{$cluetip.unbind('mouseout');}}
var direction='';$cluetipOuter.css({zIndex:$this.data('thisInfo').zIndex,overflow:defHeight=='auto'?'visible':'auto',height:defHeight});tipHeight=defHeight=='auto'?Math.max($cluetip.outerHeight(),$cluetip.height()):parseInt(defHeight,10);tipY=posY;baseline=sTop+wHeight;if(opts.positionBy=='fixed'){tipY=posY-opts.dropShadowSteps+tOffset;}else if((posX<mouseX&&Math.max(posX,0)+tipWidth>mouseX)||opts.positionBy=='bottomTop'){if(posY+tipHeight+tOffset>baseline&&mouseY-sTop>tipHeight+tOffset){tipY=mouseY-tipHeight-tOffset;direction='top';}else{tipY=mouseY+tOffset;direction='bottom';}}else if(posY+tipHeight+tOffset>baseline){tipY=(tipHeight>=wHeight)?sTop:baseline-tipHeight-tOffset;}else if($this.css('display')=='block'||link.tagName.toLowerCase()=='area'||opts.positionBy=="mouse"){tipY=bpY-tOffset;}else{tipY=posY-opts.dropShadowSteps;}
if(direction==''){posX<linkLeft?direction='left':direction='right';}
$cluetip.css({top:tipY+'px'}).removeClass().addClass('clue-'+direction+'-'+ctClass).addClass(' cluetip-'+ctClass);if(opts.arrows){var bgY=(posY-tipY-opts.dropShadowSteps);$cluetipArrows.css({top:(/(left|right)/.test(direction)&&posX>=0&&bgY>0)?bgY+'px':/(left|right)/.test(direction)?0:''}).show();}else{$cluetipArrows.hide();}
$dropShadow.hide();$cluetip.hide()[opts.fx.open](opts.fx.open!='show'&&opts.fx.openSpeed);if(opts.dropShadow){$dropShadow.css({height:tipHeight,width:tipInnerWidth,zIndex:$this.data('thisInfo').zIndex-1}).show();}
if($.fn.bgiframe){$cluetip.bgiframe();}
if(opts.delayedClose>0){closeOnDelay=setTimeout(cluetipClose,opts.delayedClose);}
opts.onShow.call(link,$cluetip,$cluetipInner);};var inactivate=function(event){isActive=false;$cluetipWait.hide();if(!opts.sticky||(/click|toggle/).test(opts.activation)){cluetipClose();clearTimeout(closeOnDelay);};if(opts.hoverClass){$this.removeClass(opts.hoverClass);}};var cluetipClose=function(){$cluetipOuter.parent().hide().removeClass();opts.onHide.call(link,$cluetip,$cluetipInner);$this.removeClass('cluetip-clicked');if(tipTitle){$this.attr(opts.titleAttribute,tipTitle);}
$this.css('cursor','');if(opts.arrows)$cluetipArrows.css({top:''});};$(document).bind('hideCluetip',function(e){cluetipClose();});if((/click|toggle/).test(opts.activation)){$this.bind('click.cluetip',function(event){if($cluetip.is(':hidden')||!$this.is('.cluetip-clicked')){activate(event);$('.cluetip-clicked').removeClass('cluetip-clicked');$this.addClass('cluetip-clicked');}else{inactivate(event);}
this.blur();return false;});}else if(opts.activation=='focus'){$this.bind('focus.cluetip',function(event){activate(event);});$this.bind('blur.cluetip',function(event){inactivate(event);});}else{$this.bind('click.cluetip',function(){if($this.attr('href')&&$this.attr('href')==tipAttribute&&!opts.clickThrough){return false;}});var mouseTracks=function(evt){if(opts.tracking==true){var trackX=posX-evt.pageX;var trackY=tipY?tipY-evt.pageY:posY-evt.pageY;$this.bind('mousemove.cluetip',function(evt){$cluetip.css({left:evt.pageX+trackX,top:evt.pageY+trackY});});}};if($.fn.hoverIntent&&opts.hoverIntent){$this.hoverIntent({sensitivity:opts.hoverIntent.sensitivity,interval:opts.hoverIntent.interval,over:function(event){activate(event);mouseTracks(event);},timeout:opts.hoverIntent.timeout,out:function(event){inactivate(event);$this.unbind('mousemove.cluetip');}});}else{$this.bind('mouseenter.cluetip',function(event){activate(event);mouseTracks(event);}).bind('mouseleave.cluetip',function(event){inactivate(event);$this.unbind('mousemove.cluetip');});}
$this.bind('mouseenter.cluetip',function(event){$this.attr('title','');}).bind('mouseleave.cluetip',function(event){$this.attr('title',$this.data('thisInfo').title);});}});};$.fn.cluetip.defaults={width:275,height:'auto',cluezIndex:97,positionBy:'auto',topOffset:15,leftOffset:15,local:false,localPrefix:null,hideLocal:true,attribute:'rel',titleAttribute:'title',splitTitle:'',escapeTitle:false,showTitle:true,cluetipClass:'default',hoverClass:'',waitImage:true,cursor:'help',arrows:false,dropShadow:true,dropShadowSteps:6,sticky:false,mouseOutClose:false,activation:'hover',clickThrough:false,tracking:false,delayedClose:0,closePosition:'top',closeText:'Close',truncate:0,fx:{open:'show',openSpeed:''},hoverIntent:{sensitivity:3,interval:50,timeout:0},onActivate:function(e){return true;},onShow:function(ct,ci){},onHide:function(ct,ci){},ajaxCache:true,ajaxProcess:function(data){data=data.replace(/<(script|style|title)[^<]+<\/(script|style|title)>/gm,'').replace(/<(link|meta)[^>]+>/g,'');return data;},ajaxSettings:{dataType:'html'},debug:false};var insertionType='appendTo',insertionElement='body';$.cluetip.setup=function(options){if(options&&options.insertionType&&(options.insertionType).match(/appendTo|prependTo|insertBefore|insertAfter/)){insertionType=options.insertionType;}
if(options&&options.insertionElement){insertionElement=options.insertionElement;}};})(jQuery);