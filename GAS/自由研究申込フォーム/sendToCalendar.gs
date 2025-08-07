function sendToCalendar(e) {
 try{
 
 //有効なGooglesプレッドシートを開く
 var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

//新規予約された行番号を取得
 var num_row = sheet.getLastRow();

//新規予約された行から名前を取得
 var nname = sheet.getRange(num_row, 3).getValue();
 
 //メールアドレスの取得
 var nmail = sheet.getRange(num_row,2).getValue();

//フリガナの取得
 var nhuri = sheet.getRange(num_row,4).getValue();

 //居住地の取得
 var npre = sheet.getRange(num_row,5).getValue();

 //市町村の取得
 var ncity = sheet.getRange(num_row,6).getValue();

 //学年の取得
 var nsho = sheet.getRange(num_row,7).getValue();

//相談方法の取得
 var nmeth = sheet.getRange(num_row,8).getValue();

 //相談内容の取得
 var ncons = sheet.getRange(num_row,9).getValue();

 //具体的な内容の取得
 var nspe = sheet.getRange(num_row,10).getValue();

 //知りましたかの取得
 var nknow = sheet.getRange(num_row,13).getValue();

 //備考の取得
 var nrem = sheet.getRange(num_row,14).getValue();

//予約を記載するカレンダーを取得(自由研究サポート申込者用)
// var cals = CalendarApp.getCalendarById("c_3738vfm7a3q6tlduq10brhon2s@group.calendar.google.com");
 var cals = CalendarApp.getCalendarById("c_5d27759fc2623dbf5485ad5672b88ea746fe62b0ea90fc9358e1b9252dc2d4e1@group.calendar.google.com");


//予約を記載するカレンダーを取得(自由研究サポートGODAC職員用詳細情報)
 var cals_details = CalendarApp.getCalendarById("c_896a8a2affa88eed56e910af2a57f7f3dc98ef0c8e5bb75ea9e1980278ad0232@group.calendar.google.com");

//予約日を取得
  var ndate = new Date(sheet.getRange(num_row, 11).getValue());

//予約の開始時間を取得
sheet.getRange(num_row, 12).setNumberFormat("h:mm:ss");
 var stime = new Date(sheet.getRange(num_row, 12).getValue());

  //予約の終了時間を取得（＊＊＊開始時間から「6０分」で指定！）
  var etime = new Date(sheet.getRange(num_row, 12).getValue());
  etime.setMinutes(etime.getMinutes()+60);//＊＊＊面談時間が6０分
 var ndates= new Date(ndate.getFullYear(),ndate.getMonth(),ndate.getDate(),stime.getHours(),stime.getMinutes(),0);
  var ndatee= new Date(ndate.getFullYear(),ndate.getMonth(),ndate.getDate(),etime.getHours(),etime.getMinutes(),0);

// 先約があるかどうか調べる
  if(cals.getEvents(ndates, ndatee)==0){
 var thing = "予約あり" ;
 
 //予約情報をカレンダーに追加(自由研究サポート申込者用)
 var r = cals.createEvent(thing, ndates, ndatee);

 //予約情報をカレンダーに追加(自由研究サポートGODAC職員用詳細情報)
 var r_details = cals_details.createEvent(num_row, nname, nmail, thing,  nhuri,  npre,  ncity,  nsho,  nmeth,  ncons,  nspe,  nknow,  nrem,  ndates,  ndatee,  stime,  etime);


 //予約日時の書式設定
var ndates = Utilities.formatDate(ndates, "JST", "yyyy'年'MM'月'dd'日'HH'時'");

// 自動返信メール件名
  var subject = '【GODAC】自由研究サポートを受け付けました。';
      
  // 自動返信メール本文

//送信者名の変更
var name = "GODAC受付"
//BCCの登録
//var bccadr = "sawanok@jamstec.go.jp,koterak@jamstec.go.jp,higashionnaa@jamstec.go.jp,oshiroa@jamstec.go.jp,kohaguraa@jamstec.go.jp,sunagawat@jamstec.go.jp,yohens@jamstec.go.jp"
var bccadr = "yohens@jamstec.go.jp"


  var body = nname + '様\n' +
    '\n' +
   '※当メールに心当たりの無い場合は、誠に恐れ入りますが\n' +
　　'　破棄して頂けますよう、よろしくお願い致します。' +
    '\n' +
    '\n' +
    '以下の内容で予約を受け付けいたしました' +
    '\n' +
    '\n' +
    '─────────────────────────\n' +
    'ご予約内容の確認\n' +
    '─────────────────────────\n' +
    '\n' +
    '【氏　　名】　' + nname + '\n' + 
    '【フリガナ　】　' + nhuri + '\n' + 
    '【居 住 地】　' + npre　+ '\n' +   
    '【市 町 村】　' + ncity　+ '\n' +    
    '【学　　年】　' + nsho　+ '\n' +  
　  '【相談方法】　' + nmeth　+ '\n' + 
　  '【相談内容】　' + ncons　+ '\n' +  
　  '【具体的な内容】　' + nspe　+ '\n' + 
    '【来館日時】　' + ndates　+ '\n' + 
    '【自由研究サポ―トをどのように知りましたか？】　' + nknow　+ '\n' +
    '【備　　考】　' + nrem　+ '\n' +
     '─────────────────────────\n' +
     '\n' +
'オンラインご希望の方は予約時間に合わせて以下のアドレスからzoomにお入りください。\n' +
　　'https://us06web.zoom.us/j/82686990932?pwd=u647gEokKalfT0bVuYGIiZIj0qv4KM.1' +
　　'\n' +
　　'※キャンセルのご連絡は電話またはメールにてご連絡ください。\n' +
　　'※事前の連絡なく15分を過ぎた場合は自動的にキャンセルとさせて頂きます。\n' +
　　'※オンラインでご参加の方は、必要な環境は各自でご準備をお願いします。\n' +
    '※本メールはシステムからの自動返信です。' +
    'お問い合わせは下記よりお願いします。\n' +
   '\n' +
    '国際海洋環境情報センター(GODAC)\n' +
　　 'TEL:0980-50-0111 E-mail: uketsuke_godac@jamstec.go.jp';
;
  
  // メール送信
  MailApp.sendEmail({
    to: nmail,
    bcc:bccadr,
    subject: subject,
    body: body,
    name:name
    
  });
}

 else{
 // 自動返信メール件名（予約できないとき）
 var name = "GODAC受付";

 //BCCの登録
//var bccadr = "sawanok@jamstec.go.jp,koterak@jamstec.go.jp,higashionnaa@jamstec.go.jp,oshiroa@jamstec.go.jp,kohaguraa@jamstec.go.jp,sunagawat@jamstec.go.jp,yohens@jamstec.go.jp"
var bccadr = "yohens@jamstec.go.jp"


  var subject = '【GODAC】予約できませんでした。';
      
  // 自動返信メール本文
  var body = nname + '様\n' +
    '\n' +
    'この度は自由研究サポートへのお申込みありがとうございました。' +
     '\n' +
    'ご希望の日時は先約があるためご予約いただけませんでした。' +
    '\n' +
    '予約カレンダーをご確認の上、ご予約日時を変更して再度お申込みください。\n' +
        '\n' +
    //'https://calendar.google.com/calendar/embed?src=c_3738vfm7a3q6tlduq10brhon2s%40group.calendar.google.com&ctz=Asia%2FTokyo\n' +
      'https://calendar.google.com/calendar/embed?src=c_5d27759fc2623dbf5485ad5672b88ea746fe62b0ea90fc9358e1b9252dc2d4e1@group.calendar.google.com&ctz=Asia%2FTokyo\n' +
            '\n' +
    '※本メールはシステムからの自動返信です。' +
    'お問い合わせは下記よりお願いします。\n' +
   '\n' +
    '国際海洋環境情報センター(GODAC)\n' +
    '休館日：月曜・祝祭日・年末年始\n' +
    'TEL:0980-50-0111\n' +
    'E-mail:uketsuke_godac@jamstec.go.jp'
;
  
  // メール送信
  MailApp.sendEmail({
    to: nmail,
    bcc:bccadr,
    subject: subject,
    body: body,
    name:name
  });
}
 
 } catch(exp){
 //実行に失敗した時に通知
 MailApp.sendEmail(nmail, exp.message, exp.message);
 }
}