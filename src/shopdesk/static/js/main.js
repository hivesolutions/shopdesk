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

            jQuery(".logo > a").click(function() {
                        var sideLinks = jQuery(".side-links");
                        sideLinks.triggerHandler("toggle");
                    });
        });
