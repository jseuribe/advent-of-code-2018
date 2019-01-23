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

function generate_order(step_list){

    var execution_str = [];

    for(step of step_list){
        console.log(step);

        if(execution_str.length == 0){
            //Base case!
            console.log("added first steps");
            execution_str.push(step[0]);
            execution_str.push(step[1]);
            console.log("new str:", execution_str);
        }
        else{
            //Carry out the proper order.
            var seen_first = false;
            var inserted_second = false;

            if(execution_str.includes(step[1])){
                execution_str.splice(execution_str.indexOf(step[1]), 1);
            }
            for(var i=0; i < execution_str.length; i++){
                var c_char = execution_str[i];
                if(c_char == step[0] && ! seen_first){
                    seen_first = true;
                    console.log("spotted first element!");
                    continue;
                }
                else if(seen_first){
                    if(c_char < step[1]){
                        //If this step is later in the alphabet, continue until we're not.
                        console.log(c_char, "Is earlier than", step[1]);
                        continue;
                    }
                    else{
                        //Otherwise, the current character is later in the alphabet; perform the insertion here!
                        console.log("splicing", step[1]);
                        execution_str.splice(i, 0, step[1]);
                        inserted_second = true;
                        break;
                        /*
                        if(i+1 == execution_str.length){
                            console.log("last element...");
                            continue;
                        } //Except if this is the last element. then just push
                        else{
                            console.log("splicing", step[1]);
                            execution_str.splice(i, 0, step[1]);
                            inserted_second = true;
                            break;

                        }
                        */

                    }
                }
            }
            if(!inserted_second){
                console.log("Pushing to end");
                execution_str.push(step[1]);
            }
            console.log("new str:", execution_str);
        }
    }
    console.log(execution_str);

    return execution_str;
}

var step_list = parseInp();

var exec_str = generate_order(step_list);

console.log(exec_str.join(""));