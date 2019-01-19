var boxcodes_fname = "inp\\boxcodes.txt"

var fs = require('fs');
    readline = require('readline');

function parseInp(){
    var boxcodes_map = new Map();
    var boxcodes_list = new Array();

    console.log("printing contents from: ", boxcodes_fname);

    /*
    var lineReader = readline.createInterface({
        input: fs.createReadStream(boxcodes_fname)
    })


    lineReader.on("line", function (line){
        console.log("Line from file:", line);
        //line_collector.push(line);
    });
    */

    var boxcodes_list = fs.readFileSync(boxcodes_fname).toString().split("\r\n");

    //console.log(boxcodes_list);   

    for(itr in boxcodes_list){
        var boxcode = boxcodes_list[itr];
        boxcodes_map.set(boxcode, new Map());
        boxcodes_map.get(boxcode).set("two_counts", 0);
        boxcodes_map.get(boxcode).set("three_counts", 0);
    }

    //console.log(boxcodes_map);
    return boxcodes_map;
}

function detCounts(boxcodes_map){

    console.log("Ahh!");
    var codes_with_two_sat = 0;
    var codes_with_three_sat = 0;

    for(const k of boxcodes_map.keys()){
        var char_map = new Map();
        console.log(k);

        for(c of k){
            if(char_map.has(c)){
                char_map.set(c, char_map.get(c) + 1);
            }
            else{
                char_map.set(c, 1);
            }
        }

        var b_two_sat = false;
        var b_three_sat = false;

        for(const c of char_map.keys()){
            if(char_map.get(c) == 2 && (! b_two_sat)){
                b_two_sat = true;
                codes_with_two_sat++;
            }
            else if(char_map.get(c) == 3 && (! b_three_sat)){
                b_three_sat = true;
                codes_with_three_sat++;
            }
        }
    }
    console.log("Codes with Two SAT:", codes_with_two_sat);
    console.log("Codes with Three SAT:", codes_with_three_sat);
    console.log("FINAL CHECKSUM:", codes_with_two_sat*codes_with_three_sat);
}

function main(){
    var boxcodes_map = parseInp();

    detCounts(boxcodes_map);
}

main();