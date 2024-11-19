$(document).ready(function() {
    $('#query').autoComplete({
        minLength: 2,
        bootstrapVersion: '4',
        noResultsText: "",
        resolverSettings: {
            fail: function() {},
            requestThrottling: 100
        }
    });

    $('#form-search').on('click', '.bootstrap-autocomplete a', function() {
        $('#form-search').submit();
    });

    $('#query').on('click', function() {
        $('#query').autoComplete('show');
    });

    $(window).resize(function(){
        // There is a bug with the plugin that messes up the drop down location 
        // when the window/page resizes. Work around it by resetting the location
        // when the window size changes
        pos = document.getElementById('query').getBoundingClientRect();
        autoCmpElem = document.getElementsByClassName('bootstrap-autocomplete')[0];
        if (autoCmpElem) {
            autoCmpElem.style.top = `${pos.bottom}px`;
            autoCmpElem.style.left = `${pos.left}px`;
            autoCmpElem.style.width = `${pos.width}`;
        }
    });
});