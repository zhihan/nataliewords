// Main app for Natlie's first words

var main = (function(){ 

    // List of different screens 
    var screens = [
        "#about",
        "#editor",
        "#slideshow",
        "#stats" ];

    var storage_name = "try"; 
    var data; // All data from the local storage

    // The data consists of a record field, which is an
    // array consisting of dates and words.

    var words = []; // The words to display
    var today = []; // Words of today
    var edit_buffer = "";
    var known = []; 

    function count() {
        var i, total;
        total = 0;
        for (i = 0; i < data.record.length; i += 1) {
            total += data.record[i].words.length;
        }
        return total;
    }

    function today_str() {
        var now = new Date(Date.now());
        var t = new Date(now.getFullYear(), now.getMonth(),
                         now.getDate());

        return t.toDateString();
    }

    function reset() {
        var i, today_rec;
        words = [];

        // Load today from the records
        var str = today_str();
        for (i =0; i < data.record.length; i +=1) {
            if (data.record[i].date === str) {
                today_rec = data.record[i];
                break;
            }
        }
        
        if (today_rec) {
            today = today_rec.words;
            edit_buffer = today.join("\n");
        } else {
            today = [];
        }
        
        for (i = 0; i < data.record.length; i += 1) {
            known.push.apply(data.record[i].words);
        }
    }

    function compute_stats() {
        var total = count();
        $("#stats").text("You have learnt " + total + " words," + " today you are learning " + today.length + " words.");
    }

    function goto_screen(screen) {
        var i;
        for (i = 0; i < screens.length; i += 1) {
            if (screens[i] === screen) {
                $(screen).removeClass("hidden");
            } else {
                $(screens[i]).addClass("hidden");
            }
        }

        if (screen === "#slideshow") {
            // refresh words
            $("#slideshow").empty();
            $("#slideshow").text(words.join(" "));
        }

        if (screen === "#edit") { 
            $("#edit_input").val(edit_buffer);
        }
    }

    function toggle_offcanvas() {
        $('.row-offcanvas').toggleClass('active');
    }
        
    function goto_about() {
        goto_screen("#about");
        toggle_offcanvas();
    }
    
    function goto_editor() {
        refresh_textarea();
        goto_screen("#editor");
        toggle_offcanvas();
    }
    
    function goto_slideshow(option) {
        if (option === "today") {
            words = today;
        }

        goto_screen("#slideshow");
        toggle_offcanvas();
    }

    function goto_stats() {
        compute_stats();
    
        goto_screen("#stats");
        toggle_offcanvas();
    }
    
    function refresh_textarea() {
        $("#edit_input").val(edit_buffer);
    }

    function store() {
        var obj = {};
        obj[storage_name] = data.record;
        chrome.storage.sync.set(obj);
    }

    function load() {
        chrome.storage.sync.get(
            storage_name,
            function after_load(o) {
                data = {record: o[storage_name]};
                reset();
            });
    }

    function get_words(text) {
        var sep = /\s/;
        var r =text.split(sep);
        return r.filter(function isempty(s) {
            return s !== "";
        });
    }
    
    function edit_change_callback() {
        var sep = /\s/;
        var today_idx = -1;
        var i;
        edit_buffer = $("#edit_input").val();
        today = get_words(edit_buffer);

        // Save today's words
        var str = today_str();
        for (i = 0; i < data.record.length; i +=1) {
            if (data.record[i].date === str) {
                today_idx = i;
                break;
            }
        }
        
        if (today_idx === -1) {
            data.record.push({
                words:today,
                date:str
            });
        } else {
            data.record[today_idx] = {
                words: today,
                date: str
            };
        }
        store();
    }


    $(document).ready(function() {
        $("#nav_about").click(goto_about);
        $("#nav_stats").click(goto_stats);
        $("#nav_editor").click(goto_editor);
        $("#nav_today").click(function() { 
            goto_slideshow("today")
        });

        $("#edit_input").change(edit_change_callback);

        load();
        goto_about();
        $('.row-offcanvas').removeClass('active');
    });

    // Initialization
    function initialize() {
        // Assume that init_data is available in the
        // global scope.
        data = {record: init_data };
        store();
    }

})();
