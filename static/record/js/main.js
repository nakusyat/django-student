function invoke_ajax_setup() {
    $.ajaxSetup({
       beforeSend: function(xhr, settings) {
           function getCookie(name) {
               var cookieValue = null;
               if (document.cookie && document.cookie != '') {
                   var cookies = document.cookie.split(';');
                   for (var i = 0; i < cookies.length; i++) {
                       var cookie = jQuery.trim(cookies[i]);
                       // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) == (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
           }
           if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
               // Only send the token to relative URLs i.e. locally.
               xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
           }
       }
    });
}

var Group = function(obj) {
    var self = this;
        self.obj = obj;
        self.group_id = obj[0].dataset.group_id;

        self.delete = function () {
            invoke_ajax_setup();
            $.ajax({
                url: "group/delete",
                type: "POST",
                data: { group_id: self.group_id },
                success: function(json) {
                    if(json.success) {
                        Materialize.toast(json.success, 4000);
                        obj.parent().parent().remove();
                    }
                },
                error: function(xhr, errmsg, err) {
                  alert(xhr.status + ": " + xhr.responseText);
                }
            });
        };

        self.edit = function() {
            var group_name_span = self.obj.siblings('span');

            var group_name_text = group_name_span.html();
                group_name_span.empty().append('<input/>');

            var input = group_name_span.children('input').val(group_name_text);
                group_name_span.append('<a data-group_id = "'+ self.group_id + '" class="group_save">Сохранить</a>');
                group_name_span.children('a').bind('click', function() {
                new Group($(this)).edit_save(input.val(), self.obj);
            });
            self.obj.hide();
        };

        self.edit_save = function(input_value, editable_obj) {
            invoke_ajax_setup();
            $.ajax({
                url: "group/edit",
                type: "POST",
                data: { group_id: self.group_id, group_name: input_value },
                success: function(json) {
                    if(json.success) {
                        Materialize.toast(json.success, 4000);
                        editable_obj.siblings('span').html(input_value);
                        editable_obj.show();
                    }
                },
                error: function(xhr, errmsg, err) {
                  alert(xhr.status + ": " + xhr.responseText);
                }
            });
        };

};

var Student = function(obj){
    var self = this;
        self.obj = obj;
        self.stud_id = obj[0].dataset.stud_id;

        self.delete = function() {
            invoke_ajax_setup();
            $.ajax({
                url: "student/delete",
                type: "POST",
                data: { stud_id: self.stud_id },
                success: function(json) {
                    if(json.success) {
                        Materialize.toast(json.success, 4000);
                        obj.parent().parent().remove();
                    }
                },
                error: function(xhr, errmsg, err) {
                  alert(xhr.status + ": " + xhr.responseText);
                }
            });
        };
        self.edit = function(){
            var stud_info_name = self.obj.siblings('span').first();
            var stud_info_surname = self.obj.siblings('span').last();
            var stud_info_birth = self.obj.parent().siblings('div').children('ul').children('li').first();
            var stud_info_stud_no = self.obj.parent().siblings('div').children('ul').children('li').last();

            var stud_info_name_text = stud_info_name.html();
            var stud_info_surname_text = stud_info_surname.html();
            var stud_info_birth_text = stud_info_birth.html();
            var stud_info_stud_no_text = stud_info_stud_no.html();

            stud_info_name.empty().append('<input/>');
            stud_info_surname.empty().append('<input/>');
            stud_info_birth.empty().append('<input/>');
            stud_info_stud_no.empty().append('<input/>');

            var input_name = stud_info_name.children('input').val(stud_info_name_text);
            var input_surname = stud_info_surname.children('input').val(stud_info_surname_text);
            var input_birth = stud_info_birth.children('input').val(stud_info_birth_text);
            var input_stud_no = stud_info_stud_no.children('input').val(stud_info_stud_no_text);
                stud_info_name.parent().append('<a data-stud_id = "'+ self.stud_id + '" class="stud_save right">Сохранить</a>');
                self.obj.parent().find('a.stud_save').bind('click', function() {
                    new Student($(this)).edit_save(input_name.val(), input_surname.val(), input_birth.val(), input_stud_no.val(), self.obj);
                });
            self.obj.hide();
        };

        self.edit_save = function(stud_name, stud_surname, stud_birth, stud_no, editable_obj){
            invoke_ajax_setup();
            $.ajax({
                url: "student/edit",
                type: "POST",
                data: { stud_id: self.stud_id, stud_name: stud_name, stud_surname: stud_surname, stud_birth: stud_birth, stud_no: stud_no },
                success: function(json) {
                    if(json.success) {
                        Materialize.toast(json.success, 4000);
                        editable_obj.siblings('span').first().html(stud_name);
                        editable_obj.siblings('span').last().html(stud_surname);
                        editable_obj.parent().siblings('div').children('ul').children('li').first().html(stud_birth);
                        editable_obj.parent().siblings('div').children('ul').children('li').last().html(stud_no);
                        editable_obj.show();
                        editable_obj.parent().find('a.stud_save').hide();
                    }
                },
                error: function(xhr, errmsg, err) {
                  alert(xhr.status + ": " + xhr.responseText);
                }
            });
        };
};

$(document).ready(function(){
    $('.group_delete').on('click', function(){ confirm('Do you want to delete?') ? new Group($(this)).delete() : false;});
    $('.group_edit').on('click', function(){ new Group($(this)).edit();});
    $('.stud_edit').on('click', function(){ new Student($(this)).edit();});
    $('.stud_delete').on('click', function(){ confirm('Do you want to delete?') ? new Student($(this)).delete(): false;});
});
