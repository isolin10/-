function doGet(e) {
  var mo = e.parameter.func;
  if (mo == "addData") {
    //set in sensor.ino
    var stat = add_data(e);
    if (stat == 1) {
      var result = {
        status: true,
      };
      return ContentService.createTextOutput(
        JSON.stringify(result)
      ).setMimeType(ContentService.MimeType.JSON);
    }
  }
}
function add_data(e) {
  var sheet = SpreadsheetApp.openByUrl("Target Sheet");
  var lastVal = sheet.getRange("A1:A").getValues();

  var CurrentDate = new Date(); //add current date in colA
  var options = {
    timeZone: "Asia/Taipei",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  };
  var Date_ = CurrentDate.toLocaleString("en-US", options);
  options = {
    timeZone: "Asia/Taipei",
    hour12: true,
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  };
  var Time_ = CurrentDate.toLocaleString("en-US", options);

  sheet.appendRow([
    Date_ + " " + Time_,
    e.parameter.temp,
    e.parameter.humd,
    e.parameter.salt,
    e.parameter.ec,
    e.parameter.ph,
    e.parameter.n,
    e.parameter.p,
    e.parameter.k,
    e.parameter.light,
  ]);
  return 1;
}
