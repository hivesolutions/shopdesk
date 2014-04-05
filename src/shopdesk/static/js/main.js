jQuery(document).ready(function() {
            jQuery(".side-links .hide").click(function() {
                        var element = jQuery(this);
                        var sideLinks = element.parents(".side-links");
                        sideLinks.triggerHandler("hide");
                    });

            jQuery(".side-links .swindow").click(function() {
                        alert("ola");
                    });


            jQuery(".side-links .side").click(function() {
                        jQuery(".side-panel").triggerHandler("toggle");
                    });
        });
