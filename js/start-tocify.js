//Executes your code when the DOM is ready.  Acts the same as $(document).ready().
$(function() {
    var titleElements = new Array();
    $('.title').each(function(){
        // Get ID of each element of class title
        var thisID = $(this).attr('id');
        var tag = $(this).prop("tagName").toLowerCase();
        // if it has an ID
        if (thisID) {
            // if it contains toc-id-*
            if (thisID.indexOf("toc-id-") >= 0){
                titleElements.push(tag + "#" + thisID);
            }
        }
    });

    tocselectors = titleElements.toString();
    console.log(tocselectors);
    //Calls the tocify method on your HTML div.
    $("#toc").tocify({
       //selectors: tocselectors
    });
});
