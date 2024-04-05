const getParam=(name,url)=>{if(!url)url=window.location.href;name=name.replace(/[\[\]]/g,"\\$&");var regex=new RegExp("[?&]"+name+"(=([^&#]*)|&|#|$)"),results=regex.exec(url);if(!results)return null;if(!results[2])return'';return decodeURIComponent(results[2].replace(/\+/g," "));};
$(function() {
  let gkey = getParam("gkey");
  let point = getParam("point");
  let macro = getParam("macro");
  switch (macro.toUpperCase()){
    case 'START':
      webiopi().callMacro("start_game", [gkey, point,]);
      $("#com").html("START");
      break;
    case 'STOP':
      webiopi().callMacro("stop_game", [gkey, point,]);
      $("#com").html("STOP");
      break;
    case 'CHECK':
      webiopi().callMacro("check_game", [gkey, point,]);
      $("#com").html("CHECK");
      break;
    default:
      console.log('error');
  }
});
