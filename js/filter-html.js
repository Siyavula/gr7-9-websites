$(function() {
    var toc = $('#toc');
    var tocids = [];
    var currentTocId = 0;
    var headings = [];
    


    // get all heading elements that match the selectors
    $('.title').each(function(){
        if ($(this).parent().prop('class') == 'section'){
            headings.push($(this));
        }
    });

    for (var i=0; i < headings.length; i++){
        var a = $('<a>' + headings[i].text() + '</a>');
        a.attr('href', '#toc-id-' + currentTocId);
        a.addClass(headings[i].prop('tagName'));

        var li = $('<p></p>');
        li.append(a);
        headings[i].prop('id', 'toc-id-' + currentTocId);
        currentTocId += 1;
        toc.append(li);
    }

    $('#toc').append(toc);
});


//
//
// The code below handles the highlighting of the current doc position in ToC.
//

// returns true if given element is in viewport
function isElementInViewport (el) {
    var rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /*or $(window).height() */
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) /*or $(window).width() */
    );
}

function elementVisibilityMayChange () {
    var tocelementIDs = [];
    var tocelements = [];

    $('#toc>p>a').each(function() {
        var href = $(this).prop('href');
        tocelementIDs.push(href.slice(href.indexOf('#')+1));
        tocelements.push($(this));
        });
    
    // Find visible element and highlight it 
    for (var i = 0; i < tocelementIDs.length; i++){
        var el = $('#' + tocelementIDs[i])[0];
        if ( isElementInViewport(el) ) {
            // remove highlight only if new element is visible.
            $('#toc>p>a').each(function() {
                $(this).removeClass('toc-highlight');
            });
            // add highlight to first visible element
            tocelements[i].addClass('toc-highlight');
            break;
        }
    }
}


//jQuery
$(window).on('DOMContentLoaded load resize scroll', elementVisibilityMayChange); 

