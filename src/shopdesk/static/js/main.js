jQuery(document).ready(function() {
            jQuery(".side-links .swindow").click(function() {
                        alert("Hello World");
                    });

            jQuery(".side-links .side").click(function() {
                        jQuery(".side-panel").triggerHandler("toggle");
                    });
        });
