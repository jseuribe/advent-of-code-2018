//https://adventofcode.com/2018/day/7

var stepsfname = "inp\\day_seven.txt"

var fs = require('fs');
    readline = require('readline');

function parseInp(){

    var stepFile = fs.readFileSync(stepsfname).toString().split("\r\n");
    var charMap = new Map();
    var steps_list = [];

    for(ln of stepFile){
        
        var action = ln[5];
        var dependency = ln[ln.length-12];
        var ctuple = [action, dependency]
        steps_list.push(ctuple);

        /*
        if(charMap.has(ctuple[0])){
            var c_arr = charMap.get(ctuple[0]);
            c_arr.push(ctuple[1]);
            charMap.set(ctuple[0], c_arr);
        }
        else{
            charMap.set(ctuple[0], [ctuple[1]]);
        }
        */
        console.log(charMap);

    }

    return steps_list;

}

function generate_char_list(step_list){
    var all_chars = [];

    for(step of step_list){
        if(!all_chars.includes(step[0])){
            all_chars.push(step[0]);
        }

        if(!all_chars.includes(step[1])){
            all_chars.push(step[1]);
        }

    }
    
    return all_chars.sort();
}

function generate_grid_map(chars){
    var map = new Map();

    for(char of chars){
        var these_edges = new Map();
        for(edge_char of chars){
            these_edges.set(edge_char, false);
        }

        map.set(char, these_edges);
    }

    return map;
}

function determine_connections(step_list, graph){
    for(step of step_list){
        graph.get(step[0]).set(step[1], true);
    }
    return graph;
}

function isEmpty(map){
    var list = map.keys();
    var count = 0;

    for(key of list){
        count++;
    }
    return count == 0;
}

function find_path(graph){

    var exec_steps = [];
    while(!(isEmpty(graph))){
        var candidates = [];
        for(node of graph.keys()){
            var c_count = 0;
            for(conn_node of graph.keys()){
                if(conn_node == node){
                    continue;
                }
                else{
                    var c_arr = graph.get(conn_node);
                    //console.log("EXAMINING", conn_node, "FOR CONNECTIVITY TO:", node);
                    //console.log(c_arr);

                    if(c_arr.get(node)){
                        //console.log("A NODE IS CONNECTED TO:", node)
                        c_count++;

                    }
                }
            }

            if(c_count == 0){
                candidates.push(node);
            }
        }

        candidates.sort();
        //console.log("CANDIDATE FOR REMOVAL:", candidates[0]);
        exec_steps.push(candidates[0]);
        graph.delete(candidates[0]);
    }

    console.log("FINAL STEPS:", exec_steps.join(""));
}

var step_list = parseInp();

var all_chars = generate_char_list(step_list);

//console.log(all_chars);

var graph = generate_grid_map(all_chars);

determine_connections(step_list, graph);

find_path(graph);