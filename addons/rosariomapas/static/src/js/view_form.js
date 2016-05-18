openerp.rosariomapas = function(instance){
    var QWeb = instance.web.qweb,
    _t = instance.web._t;
    
    

    openerp.web.form.WidgetIconM2O = instance.web.form.FieldMany2One.extend({
        display_string: function(str) {
            var self = this;
            var name = str;
            console.log(str);
            if (str)
                name = str.split("/")[str.split("/").length -1];
            if (!this.get("effective_readonly")) {
                this.$input.val(name.split("\n")[0]);
                this.current_display = this.$input.val();
                if (this.is_false()) {
                    this.$('.oe_m2o_cm_button').css({'display':'none'});
                } else {
                    this.$('.oe_m2o_cm_button').css({'display':'inline'});
                }
            } else {
                var lines = _.escape(name).split("\n");
                var link = "asd";
                var follow = "dsa";
                link = lines[0];
                follow = _.rest(lines).join("<br />");
                if (follow)
                    link += "<br />";
                var $link = this.$el.find('.oe_form_uri')
                     .unbind('click')
                     .html("<img src='"+str+"'/>" + link);
                if (! this.options.no_open)
                    $link.click(function () {
                        var context = self.build_context().eval();
                        var model_obj = new instance.web.Model(self.field.relation);
                        model_obj.call('get_formview_action', [self.get("value"), context]).then(function(action){
                            self.do_action(action);
                        });
                        return false;
                     });
                $(".oe_form_m2o_follow", this.$el).html(follow);
            }
        },
    });
    instance.web.form.widgets.add('widget_icon_m2o', 'openerp.web.form.WidgetIconM2O');
}