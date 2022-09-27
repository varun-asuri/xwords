const fetch = require("node-fetch");
const https = require("https");

let url = "https://www.google.com/async/dictw?hl=es&async=term:hola,corpus:es,hhdr:false,hwdgt:true,wfp:true,xpnd:true,ttl:,tsl:es,_id:dictionary-modules,_pms:s,_jsfs:Ffpdje,_fmt:pc"

/*
const getData = async url => {
    const response = await fetch(url);
    console.log(response);
}

getData(u);
*/

const r2 = require("r2");
//const url = "https://jsonplaceholder.typicode.com/posts/1";

const getData = async url => {
  try {
    const response = await r2(url).text;
    console.log(response);
  } catch (error) {
    console.log(error);
  }
};

getData(url);