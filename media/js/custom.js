/* 
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
$.extend({
    'mobile':function(){
        return !$.browser.msie && !$.browser.mozilla && !$.browser.opera && !$.browser.safari && !$.browser.flock && !$.browser.linux && !$.browser.mac && !$.browser.win 
    }
}) 
function searchFormTabs(arr0){
  var arr=arr0
  var tabs_relative=$('<div id="search_form_tabs_relative">').html('&nbsp;')
  var tabs_holder=$('<div id="search_form_tabs"></div>')
  var tabs=$([])
  var last_form=$([])
  for(var i=0;i<arr.length;i++){
    var form=$('#'+arr[i].id)
    if(form.length<1){
      alert('cannot find form '+arr[i].id)
    }
    if(i==0){
      tabs_relative.insertBefore(form)
      tabs_holder.appendTo(tabs_relative)
      last_form=last_form.add(form)
    }
    else{
      form.hide()
    }

    var tab=$('<a></a>').attr('href','#').data('form',form).html(arr[i].text).click(function(e){
      e.preventDefault()

      last_tab.removeClass('selected')
      last_form.hide()

      $(this).data('form').show()
      $(this).addClass('selected')

      last_tab=$(this)
      last_form=$(this).data('form')
      $.cookie('search_form',tabs.index(this),{path:'/'})

    }).appendTo(tabs_holder)

    if(i==0){
      tab.addClass('selected')
      last_tab=tab
    }
    tabs=tabs.add(tab)
  }
  if($.cookie('search_form')){
    tabs.eq($.cookie('search_form')).triggerHandler('click')
  }

}

function updateModel2(json0){
  if(!typeof(json0) == 'object'){
    alert('updatemodel2 - 1st argument must a json object')
    return 0
  }
  if(!typeof(json0.form) == 'string'){
    alert('updatemodel2 - json object must have "form"')
    return 0
  }
  if(!typeof(json0.model) == 'string'){
    alert('updatemodel2 - json object must have "model"')
    return 0
  }
  if(!typeof(json0.brand) == 'string'){
    alert('updatemodel2 - json object must have "brand"')
    return 0
  }

  var form=$(json0.form)
  if(!form.length){
    alert('updatemodel2 - '+json0.form+' not found')
    return 0
  }

  var model_select=form.find(json0.model)
  if(model_select.length<1){
    alert('updatemodel2 - '+json0.model+' not found')
    return 0
  }

  var model_options=model_select.find('option[name]')
  if(!model_options.length){
     //if no options with attribute 'name'
     alert('updatemodel2 - options must have name attributes to represent foreign key value in '+json0.model)
     return 0
  }
  var brand_select=form.find(json0.brand)
  if(brand_select.length<1){
     alert('updatemodel2 - cannot find brand '+json0.brand)
     return 0
  }

  /*
   *  Removed ability to HIDE options, because in firefox, u can still select hidden options with arrow keys
   */

  //create fake select
  fake_select=$('<select id="fake_select"></select>').appendTo('body').hide()

  var last_model_options=null;

  var selected_option=model_options.filter('option:selected') //get selected
  if(selected_option.length>0){
    //if model is selected on load, select related brand/group
    brand_select.val(selected_option.attr('name'))
    model_options.filter('[name!='+brand_select.val()+']').appendTo(fake_select)
    //eg. last selected options were all toyota models
    last_model_options=model_select.find('option[name]')
  }
  else if(brand_select.val()){
    //if brand is selected on load, hide all except preselected by brand value
    model_options.filter('[name!='+brand_select.val()+']').appendTo(fake_select)
    //eg. last selected options were all toyota models
    last_model_options=model_select.find('option[name]')
  }
  else{
    //if no brand selected on load, disable model select box and hide all options
    model_select.attr('disabled',true)

    //create fake select and dump all model_options to it
    model_options.appendTo(fake_select)
  }
  //var temp = $(json0.temp_value)
  brand_select.change(function(e){
    var brand_option_val=$(this).val()
    if(brand_option_val){
      //chosen brand has a value, so show model select options
      model_select.removeAttr('disabled')

      if(last_model_options && last_model_options.length){
        //if previous visible options exists, hide them
        //append previous model options to hidden fake select
        last_model_options.appendTo(fake_select)
      }

      //get selected model options
      last_model_options=model_options.filter('[name='+brand_option_val+']')

      last_model_options.appendTo(model_select)

      //select blank option
      //if(temp=='')
      model_select.val('')
      //else model_select.val(temp)
    }
    else{
      //no brand value, so disable model select options
      model_select.attr('disabled',true)
    }
  })

}

function updateModel3(json0){
  if(!typeof(json0) == 'object'){
    alert('updatemodel2 - 1st argument must a json object')
    return 0
  }
  if(!typeof(json0.form) == 'string'){
    alert('updatemodel2 - json object must have "form"')
    return 0
  }
  if(!typeof(json0.model) == 'string'){
    alert('updatemodel2 - json object must have "model"')
    return 0
  }
  if(!typeof(json0.brand) == 'string'){
    alert('updatemodel2 - json object must have "brand"')
    return 0
  }

  var form=$(json0.form)
  if(!form.length){
    alert('updatemodel2 - '+json0.form+' not found')
    return 0
  }

  var model_select=form.find(json0.model)
  if(model_select.length<1){
    alert('updatemodel2 - '+json0.model+' not found')
    return 0
  }

  var model_options=model_select.find('option[name]')
  if(!model_options.length){
     //if no options with attribute 'name'
     alert('updatemodel2 - options must have name attributes to represent foreign key value in '+json0.model)
     return 0
  }
  var brand_select=form.find(json0.brand)
  if(brand_select.length<1){
     alert('updatemodel2 - cannot find brand '+json0.brand)
     return 0
  }

  /*
   *  Removed ability to HIDE options, because in firefox, u can still select hidden options with arrow keys
   */

  //create fake select
  fake_select=$('<select id="fake_select"></select>').appendTo('body').hide()

  var last_model_options=null;

  var selected_option=model_options.filter('option:selected') //get selected
  if(selected_option.length>0){
    //if model is selected on load, select related brand/group
    brand_select.val(selected_option.attr('name'))
    model_options.filter('[name!='+brand_select.val()+']').appendTo(fake_select)
    //eg. last selected options were all toyota models
    last_model_options=model_select.find('option[name]')
  }
  else if(brand_select.val()){
    //if brand is selected on load, hide all except preselected by brand value
    model_options.filter('[name!='+brand_select.val()+']').appendTo(fake_select)
    //eg. last selected options were all toyota models
    last_model_options=model_select.find('option[name]')
  }
  else{
    //if no brand selected on load, disable model select box and hide all options
    model_select.attr('disabled',true)

    //create fake select and dump all model_options to it
    model_options.appendTo(fake_select)
  }
  //var temp = $(json0.temp_value)
  brand_select.change(function(e){
    var brand_option_val=$(this).val()
    if(brand_option_val){
      //chosen brand has a value, so show model select options
      model_select.removeAttr('disabled')

      if(last_model_options && last_model_options.length){
        //if previous visible options exists, hide them
        //append previous model options to hidden fake select
        last_model_options.appendTo(fake_select)
      }

      //get selected model options
      temp_data = fake_select
      last_model_options=model_options.filter('[name='+brand_option_val+']')

      last_model_options.each(function(e){
          data=model_select.filter(':contains('+$(this).html()+')')
          if(!data.length){
              $(this).appendTo(model_select)
              //alert('bs')
          }
      })
     // alert(temp_data.html())

      //select blank option
      //if(temp=='')
      model_select.val('')
      //else model_select.val(temp)
    }
    else{
      //no brand value, so disable model select options
      model_select.attr('disabled',true)
    }
  })
}
function index_js(){
        
        $('#id_user_email').attr('size','60')
        var div_warning = $('<div align="center" id="pop_up_msg" style="overflow: hidden; width: 100%; font-size: 20px; height: 30px;color:red;">Please wait while we processing your request.</div>')

        $('.log_in2').click(function(e){
            if($("#id_user_email").val()!="")
            {
                $(this).hide();
                $('<img src="/media/img/preloader-small.gif" style="margin-top:5px;"/>').insertAfter($(this))
                $("#email_parent").append(div_warning)
            }
        })


        $('#pop_up_ad').click(function(){
            $('#pop_up_ad').hide()
        })
        $('#size_pop_up').hide()
        $('#size_guide').click(function(e){
            e.preventDefault()
            $('#size_pop_up').show()
        })
        $('#close_size').click(function(e){
            e.preventDefault()
            $('#size_pop_up').hide()
        })
        $('#submit_ideal').click(function(e){
            e.preventDefault()
            var feet =$('#ibw_height_feet')
            var weight=$('#ibw_weight')
            var heightFeet = parseInt(feet.val());
            var weight_val = parseInt(weight.val());
            var frame = $('.frame')
            var frame_val;
            var data= false
            var idealWeight = 0.9*heightFeet - 88;
           // var  idealWeight = (((((heightFeet * 12) ) - 60) * 6) + 106);
            $('.frame').each(function(e){
                if($(this).attr('checked')){data=true;frame_val=$(this).val()}
            })
            if(feet.val()==''){
                alert('Please fill your height.')
                feet.focus()
                feet.attr('style','background-color:red;')
            }
            else if(weight.val()==''){
                alert('Please fill your weight')
                weight.focus()
                weight.attr('style','background-color:red;')
            }
            else if(data==false){
                alert('Please choose your frame size')
            }
            else{
                if(frame_val==1){
                    frameSize = "Small";
                    idealWeight = parseInt(idealWeight) - 10;
                }
                if(frame_val==2){frameSize="Medium";}
                if(frame_val==3){
                    frameSize = "Large";
                    idealWeight = parseInt(idealWeight) + 10;
                }
                var maxIdealWeight = Math.round((parseInt(idealWeight) * 1.1)*100)/100 ;
                var overWeightBy = Math.round((weight_val - parseFloat(maxIdealWeight))*100 )/100 ;
                var difference = parseFloat(overWeightBy) + ' lbs. (' + Math.round(((overWeightBy)*100)/100) + ' kg.).';

                var weightRange = Math.round((idealWeight)*10)/10 + ' - ' + Math.round((maxIdealWeight)*100 )/100  + ' kg.';
                idealWeight = weight_val / idealWeight;
                idealWeight = Math.round(idealWeight*100)/100;
                if ((idealWeight >= 1.00) && (idealWeight <= 1.10))
                    IBWCalculation = "Contratulations! Your weight is ideal!";
                else if ((idealWeight > 1.10) && (idealWeight < 1.20))
                    IBWCalculation = "You are marginally overweight by " + difference;
                else if ((idealWeight >= 1.20) && (idealWeight <= 1.30))
                    IBWCalculation = "You are overweight by " + difference;
                else if (idealWeight > 1.30)
                    IBWCalculation = "You are overweight by " + difference + "<br>You may wish to consult with your physician for medical help.";
                else
                    IBWCalculation = "You are underweight.";
                IBWCalculation = '<div style="overflow:hidden;height:145px;" id="ideal_res">'+"Ideal weight range is " + weightRange + '<br>' + IBWCalculation+'<br> --is based on a formula that calculates what a healthy weight is for most people of your height ('+heightFeet+') and frame size ('+frameSize+').' +'</div><div><a href="#" id="back_ideal" class="short_red_button">back</a></div>';
                $('#ideal_res').html(IBWCalculation)
		  $('#ideal_res').show()
                $('#ideal_form').hide()
            }
            $('#back_ideal').click(function(e){
                        e.preventDefault()
                        $('#ideal_res').hide()
                        $('#ideal_form').show()
                        $('#back_ideal').attr('style','display:none;')
                    })
        })

        if(click_value == 1){
            $('#view').addClass('selected')
        }
        else if(click_value == 2)
        {
            $('#comment').addClass('selected')
            $('#view').removeClass('selected')
        }
        else if(click_value == 3)
        {
            $('#favorite').addClass('selected')
            $('#view').removeClass('selected')
           // $('#asd').attr('style','height:210px;')
        }
        else if(click_value == 4)
        {
            $('#updated').addClass('selected')
            $('#view').removeClass('selected')
            //$('#asd').attr('style','height:210px;')
        }
        else
        {
            $('#invite').addClass('selected')
            $('#view').removeClass('selected')
        }

        $('#row_pic1').animate( { top:"0px" } , 300 )
        $('#row_pic2').animate( { top:"0px" } , 300 )
        $('#row_pic3').animate( { top:"0px" } , 300 )
        $('#row_pic4').animate( { top:"0px" } , 300 )
        if(!$.mobile()){
        var a =$(".initial").val()
        /*$('.ads_for_index li').hover(
          function () {
              var get_flash_url = $(this).children().children().children('#flash_ad').val()
              var MEDIA_URL = "/media/"
              var src_flash_picture = MEDIA_URL+get_flash_url
              $(this).children().children().stop().animate( { top:"-30px" } , 300 )
              $('.flash_picture').stop().animate({ "height": "toggle", "opacity": "toggle"}, {  "duration": "slow"})
              $('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {  "duration": "slow"}).attr('src',src_flash_picture)
          },
          function () {
            $(this).children().children().stop().animate( { top:"0px" } , 300 )
          }
        );*/
        hiConfig = {
        sensitivity: 7,
        interval: 150,
        timeout: 100,
        over: function(){
                $('#row_pic2').animate( { top:"0px" } , 300 )
                $('#row_pic3').animate( { top:"0px" } , 300 )
                $('#row_pic4').animate( { top:"0px" } , 300 )
                if(a != 1){
                    var get_flash_url = $("#row_pic1 input").val()
                    var MEDIA_URL = "/media/"
                    var src_flash_picture = MEDIA_URL+get_flash_url
                    $('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {"duration": "fast"})
                    $('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {  "duration": "slow"}).attr('src',src_flash_picture)
                    $('#row_pic1').animate( { top:"-30px" } , 300 )
                    a=1
                }

            },
            out:function(){

                if(a != 1){
                var get_flash_url = $("#row_pic1 input").val()
                var MEDIA_URL = "/media/"
                var src_flash_picture = MEDIA_URL+get_flash_url
                //$('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {  "duration": "slow"}).attr('src',src_flash_picture)
                $('#row_pic1').animate( { top:"-30px" } , 300 )
                 //   a=1
               }

            }
    }
    $('#row_pic1').hoverIntent(hiConfig)


        hiConfig = {
        sensitivity: 7,
        interval: 150,
        timeout: 100,
        over: function(){
                $('#row_pic1').animate( { top:"0px" } , 300 )
                $('#row_pic3').animate( { top:"0px" } , 300 )
                $('#row_pic4').animate( { top:"0px" } , 300 )
                if(a != 2){

                    $('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {"duration": "fast"})
                    var get_flash_url = $("#row_pic2 input").val()
                    var MEDIA_URL = "/media/"
                    var src_flash_picture = MEDIA_URL+get_flash_url
                    $('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {  "duration": "slow"}).attr('src',src_flash_picture)
                    $('#row_pic2').animate( { top:"-30px" } , 300 )
                    a=2
                }

            },
            out:function(){
                if(a != 2){
                var get_flash_url = $("#row_pic2 input").val()
                var MEDIA_URL = "/media/"
                var src_flash_picture = MEDIA_URL+get_flash_url
               // $('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {  "duration": "slow"}).attr('src',src_flash_picture)
                $('#row_pic2').animate( { top:"-30px" } , 300 )
                   // a=2
                }

            }
    }
    $('#row_pic2').hoverIntent(hiConfig)

        hiConfig = {
        sensitivity: 7,
        interval: 150,
        timeout: 100,
        over: function(){
                $('#row_pic2').animate( { top:"0px" } , 300 )
                $('#row_pic1').animate( { top:"0px" } , 300 )
                $('#row_pic4').animate( { top:"0px" } , 300 )
                if(a != 3){
                    $('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {"duration": "fast"})
                    var get_flash_url = $("#row_pic3 input").val()
                    var MEDIA_URL = "/media/"
                    var src_flash_picture = MEDIA_URL+get_flash_url
                    $('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {  "duration": "slow"}).attr('src',src_flash_picture)
                    $('#row_pic3').animate( { top:"-30px" } , 300 )
                    a=3
                }

            },
            out:function(){
                if(a != 3){
                var get_flash_url = $("#row_pic3 input").val()
                var MEDIA_URL = "/media/"
                var src_flash_picture = MEDIA_URL+get_flash_url
                //$('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {  "duration": "slow"}).attr('src',src_flash_picture)
                $('#row_pic3').animate( { top:"-30px" } , 300 )
                    //a=3
                }

            }
    }
    $('#row_pic3').hoverIntent(hiConfig)

        hiConfig = {
        sensitivity: 7,
        interval: 150,
        timeout: 100,
        over: function(){
                $('#row_pic2').animate( { top:"0px" } , 300 )
                $('#row_pic3').animate( { top:"0px" } , 300 )
                $('#row_pic1').animate( { top:"0px" } , 300 )
                if(a != 4){
                    $('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {"duration": "fast"})
                    var get_flash_url = $("#row_pic4 input").val()
                    var MEDIA_URL = "/media/"
                    var src_flash_picture = MEDIA_URL+get_flash_url
                    $('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {  "duration": "slow"}).attr('src',src_flash_picture)
                    $('#row_pic4').animate( { top:"-30px" } , 300 )
                    a=4
                }

            },
            out:function(){
                if(a != 4){
                var get_flash_url = $("#row_pic4 input").val()
                var MEDIA_URL = "/media/"
                var src_flash_picture = MEDIA_URL+get_flash_url
                //$('.flash_picture').animate({ "height": "toggle", "opacity": "toggle"}, {  "duration": "slow"}).attr('src',src_flash_picture)
                $('#row_pic4').animate( { top:"-30px" } , 300 )
                //    a=4
                }

            }
    }
    $('#row_pic4').hoverIntent(hiConfig)
        }
}

function acc_base_js(){
    
    $('#dropdown2').hide()
       $(".sf-menu").superfish({
                animation: {height:'show'},   // slide-down effect without fade-in
                delay:     2000               // 1.2 second delay on mouseout
            });
        $('#all_col').click(function(e){
               e.preventDefault()
            }
        )
        if (window.attachEvent) window.attachEvent("onload", sfHover);

               $('#clickme').cluetip({activation: 'click', sticky: true,closePosition: 'title', width: 350, splitTitle: '|'});
               $('#side_add_collection_clickme').cluetip({activation: 'click', sticky: true,closePosition: 'title', width: 350, splitTitle: '|'});
}

function detail_items_js(){
    $('#addict_clickme').cluetip({activation: 'click', sticky: true,closePosition: 'title', width: 350, splitTitle: '|'});
    $('#compare_clickme').cluetip({activation: 'click', sticky: true,closePosition: 'title', width: 350, splitTitle: '|'});
    $('#id_comment').css('width','372px')
    $('#id_comment').css('height','100px')
    $('#bottom_ad').hide();
    $('#change_img').attr('style','cursor:pointer');
    $('#change_img1').attr('style','cursor:pointer');
    all.show();
    if('{{item.line.store.user.id}}'=='{{user.id}}'){
        img.attr('style','display:;border:none;');
        name1.attr('style',' color:#B5121C; font-weight:bold; margin-left:0px')
        img.attr('src','/media/fashion_icon.png');
    }
        
    $('#product_picture').click(function(e){
        e.preventDefault()
        $('#detail_picture').removeAttr('style')
        $('#detail_picture').attr('style','display:block;position:absolute;top:295px;z-index:2000;background-color:white;height:500px;')

    })
    $('.close').click(function(e){
        e.preventDefault()
        $('#detail_picture').attr('style','display:none')
    })
    
    $('#example-1').ratings(5).bind('ratingchanged', function(event, data) {
    $('#example-rating-1').text(data.rating);

  });
      $('#form1').submitLoad()
      
}

function compare_thumb_js(){
    if(!$.mobile()){
        store1.click(function(){
        all1.hide();
        unhide.attr('src','');

        name2.attr('style',' color:#B5121C; font-weight:bold;')
    })

    unhide.attr('style','display:;border:none;');
    all1.show();
    unhide.attr('src','/media/fashion_icon.png');
    name2.attr('style',' color:#B5121C; font-weight:bold;')

        
  //robin added
  //you can get MANY classes, but you can get only ONE id
  //that's why I created class="star_counter_class"
  $('.star_counter_class').each(function(i){
    var stars=$([]) //empty jquery
    var input_value=$(this).val()
    if(input_value!=0){
    for(var i=0;i<input_value;i++){
      $('<img src="/media/full-star.png" />').insertBefore($(this))

    }
          if(input_value!=5)
          {
              for(var a=input_value;a<5;a++){
                  $('<img src="/media/empty-star.png" />').insertBefore($(this))

              }

          }
    }
    else{
                      for(var a=input_value;a<5;a++){
                  $('<img src="/media/empty-star.png" />').insertBefore($(this))

              }
    }
  })

       
        $('#uncheck_all').click(
          function(e){
            e.preventDefault()
            $('.input').attr('checked',false)
          }
        )
     }
}

function view_detail_compare_js(){
    if(!$.mobile()){
    unhide.attr('style','display:;border:none;');
    all1.show();
    unhide.attr('src','/media/fashion_icon.png');
    name2.attr('style',' color:#B5121C; font-weight:bold;')

  $('.horoscopePanel').hide();
  $('.horoscopePanel1').hide();
  $('.description a').click(function(e){
      e.preventDefault()
  })

  $('.location a').click(function(e){
      e.preventDefault()

  })


  $('.side_menu_box').attr('style','height:860px;')
  $('.star_counter_class').each(function(i){
    var stars=$([]) //empty jquery
    var input_value=$(this).val()
    if(input_value!=0){
    for(var i=0;i<input_value;i++){
      $('<img src="/media/full-star.png" />').insertBefore($(this))

    }
          if(input_value!=5)
          {
              for(var a=input_value;a<5;a++){
                  $('<img src="/media/empty-star.png" />').insertBefore($(this))

              }

          }
    }
    else{
                      for(var a=input_value;a<5;a++){
                  $('<img src="/media/empty-star.png" />').insertBefore($(this))

              }
    }

  })
           var new_location1 = $('.location a').each(function(i){
            $(this).click(function(a){
                $('.horoscopePanel1').each(function(d){
                    //console.log($(this))
                    $(this).hide();
                    var test1 = $(this).html()
                    $(this).html(test1);
                    $('.close1').click(function(e){
                        e.preventDefault();
                        $(this).parent().parent().hide();
                    })
                })

                //$(this).next($('.horoscopePanel').hide
                $(this).next('.horoscopePanel1').toggle()

            })

        })
                var new_location = $('.description a').each(function(i){
                $(".cross1").each(function(f){
                $(this).attr('src','/media/cross.png');
                });
            $(this).click(function(a){
                $('.horoscopePanel').each(function(e){

                    $(this).hide();

                    var test = $(this).html()
                    $(this).html(test);
                    $('.x_close').click(function(e){e.preventDefault(); $(this).parents('.horoscopePanel').hide();})
                })

                //$(this).next($('.horoscopePanel').hide
                $(this).next().toggle()

            })

        })
        }
}

function notification_js(){
    if(!$.mobile()){
        $('#store1').click(function(){
        all2.hide();
        expand.attr('src','');

        name3.attr('style',' color:#B5121C;font-weight:bold; margin-left:20px')
        })
        $('#id_select').change(function(e){
            $('#form1').submit();
        })
        expand.attr('style','display:inline;border:none;');
        all2.show();
        expand.attr('src','/media/fashion_icon.png');
        name3.attr('style',' color:#B5121C; font-weight:bold; margin-left:0px')
        $("input[name=topics]").click(function(){
        var length=$(this).length
        if($("input[name=topics]").length!=$("input[name=topics]:checked").length){
         $(".checkall").each(function()
            {
                $(this).attr('checked',false)
            });
          }
        });
         $('.checkall').click(function(){
                    var checked_status = this.checked;
                    $(".checkall").each(function(){
                        this.checked = checked_status;


                    });

                    $("input[name=topics]").each(function()
                    {
                        this.checked = checked_status;


                    });
            })
            }
}

function send_items_js(){
    store1.click(function(){
        all2.hide();
        expand.attr('src','');

        name3.attr('style',' color:#B5121C;font-weight:bold; margin-left:20px')
        })
        if(!$.mobile()){
        $('#id_select').change(function(e){
            $('#form1').submit();
        })
        expand.attr('style','display:;border:none;');
        all2.show();
        expand.attr('src','/media/fashion_icon.png');
        name3.attr('style',' color:#B5121C; font-weight:bold; margin-left:0px')
        $("input[name=topics]").click(function(){
        var length=$(this).length
        if($("input[name=topics]").length!=$("input[name=topics]:checked").length){
         $(".checkall").each(function()
            {
                $(this).attr('checked',false)
            });
          }
        });
         $('.checkall').click(function(){
                    var checked_status = this.checked;
                    $(".checkall").each(function(){
                        this.checked = checked_status;


                    });

                    $("input[name=topics]").each(function()
                    {
                        this.checked = checked_status;


                    });
            })
            }
}

function edit_profile_js(){
    if($('#id_country').val()!="1"){
            $('#id_province').attr('disabled',true);
        }
        var prof_img = $('#profile_img')
        var prof = $('#name7')
        prof_img.attr('style','display:;border:none;');
        prof_img.attr('src','{{MEDIA_URL}}fashion_icon.png');
        prof.attr('style',' color:#B5121C; font-weight:bold;')
        updateModel2({form:'#edit_form',model:'#id_province',brand:'#id_country'})
        updateModel2({form:'#edit_form',model:'#id_phone_area_code',brand:'#id_province'})
        updateModel2({form:'#edit_form',model:'#id_fax_area_code',brand:'#id_province'})
        $('#column9').hide()
        $('#id_phone_area_code').insertAfter($('#columnb10'))
        $('#column12').hide()
        $('#id_fax_area_code').insertAfter($('#columnb13'))
        $("#id_date_of_birth").datepicker({ showAnim: 'slideDown' ,altField: '#id_date_of_birth',altFormat: 'dd/mm/yy',changeMonth: true, changeYear: true, minDate: new Date(1950, 0,1),maxDate: new Date(2000, 12, 0), yearRange: '1950:2000',defaultDate:  new Date(1950, 0, 1),showOn: 'button', buttonImage: '{{ MEDIA_URL}}css/images/calendar.gif', buttonImageOnly: true});
        $('.side_menu_box').css('height','1010px')
        $('#column18').attr('style','width:300px;')
        $('#id_date_of_birth').attr('readonly',true)
        $('#id_telephone').numeric({allow:"+"});
        $('#id_post_code').numeric();
        $('#id_handphone').numeric({allow:"+"});
        $('#id_fax').numeric({allow:"+"});
        $('#id_country').change(function(){
            if($(this).val()=="1"){
                $('#id_phone_area_code').attr('disabled',false);
                $('#id_fax_area_code').attr('disabled',false);
            }else{
                $('#id_province').attr('disabled',true);
                $('#id_phone_area_code').attr('disabled',true);
                $('#id_fax_area_code').attr('disabled',true);
            }
        })
        fieldlimiter.setup({
            thefield: document.getElementById("id_street_address"), //reference to form field
            maxlength: 100,
            statusids: ["eg5"], //id(s) of divs to output characters limit. If non, set to empty array [].
            onkeypress:function(maxlength, curlength){ //onkeypress event handler
                //define custom event actions here if desired
            }
        })
        fieldlimiter.setup({
            thefield: document.getElementById("id_about_me"), //reference to form field
            maxlength: 1000,
            statusids: ["eg16"], //id(s) of divs to output characters limit. If non, set to empty array [].
            onkeypress:function(maxlength, curlength){ //onkeypress event handler
                //define custom event actions here if desired
            }
        })
}