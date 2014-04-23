(function ($) {
    $.fn.tableofcontents = function(options) {
        var settings = $.extend({
            id: "container", // target element id
            css: {
                "padding": "3px", // padding size
                "border": "solid 1px #CCC", // border style
                "width": null // width
            }
        }, options);

        options = $.extend(settings, options);
        
        var target = $(options.id)
            .append($("<div></div>").html("Contents").css({ "font-weight": "bold" }))
            .append("<ul></ul>")
            .css(options.css);
            
        var prevLevel = 0;
        var getLevel = function(tagname) {
            switch(tagname) {
                case "H1": return 1;
                case "H2": return 2;
                case "H3": return 3;
                case "H4": return 4;
                case "H5": return 5;
                case "H6": return 6;
            }

            return 0;
        };

        var getUniqId = function() {
            return "__toc_id:" + Math.floor(Math.random() * 100000);
        };

        this.find("h1, h2, h3, h4, h5, h6").each(function() {
            var that = $(this);
            var currentLevel = getLevel(that[0].tagName);
            if(currentLevel > prevLevel) {
                var tmp = $("<ul></ul>").data("level", currentLevel);
                target = target.append(tmp);
                target = tmp;
                
            }else {
                while(target.parent().length && currentLevel <= target.parent().data("level")) {
                    target = target.parent();
                }
            }

            var txt = that.html();
            var txtId = that.attr("id");
            if(!!!txtId) {
                txtId = getUniqId();
                that.attr({ "id": txtId });
            }

            var alink = $("<a></a>").text(txt).attr({ "href": "#" + txtId });
            target.append($("<li></li>").append(alink));
            prevLevel = currentLevel;
        });
        
        return this;
    };
}(jQuery));
