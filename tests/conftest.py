import pytest

from phaseIV import PhaseivClient
from phaseIV.scrapper.parser import Film, Status


@pytest.fixture
def search_title():
    return "Soul"

@pytest.fixture
def search_html():
    """Page source for search with search_title."""
    return """
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="/css/iv5.css" type="text/css">
<link rel="SHORTCUT ICON" href="https://www.filmgalerie-phaseiv.de/png/AmeiseWeb_hgTransp_300px.png">
<title> Filmgalerie Phase IV - Suchen </title>
  <script type="text/javascript" src="/js/navigator5.js"></script>
  <script type="text/javascript" src="/js/prototype.js"></script>
  <script type="text/javascript" src="/js/footer5.js"></script>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="Author" content="DB+GNU Emacs+w3schools">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link rel="stylesheet" href="/notfall.css" type="text/css"></head>

<body onload="navigator5(); footer5();"> <img class="notfall" src="/png/notfall.png" />

  <nav>
    <div id="navigator5"></div>
  </nav>

  <div class="main">

        Unsere Suche unterst&uuml;tzt eine m&ouml;glichst breite
        Datenabfrage, zum Beispiel in Form von Einzelw&ouml;rtern des Titels,
        von Namen der Regisseure und Schauspieler oder den Erscheinungsjahren
        der Filme.

<p style="margin: 10px;margin-top:25px;">
<form action="/cgi-bin/suchen5.pl" name=suchform method="post">
<input type=hidden name=noajax value=1>
<table>
<tr><td><input type="text" size=20 id=search name="s"></td></tr>
<tr><td align='right'><input type="submit" value="Suchen"></td></tr>
</table>
</form></p><script language="JavaScript">
new Form.Element.Observer('search', 0.5, function(element, value) {
    new Ajax.Updater('mainmatter', 'suchen5.pl',
    {asynchronous:true, evalScripts:true, parameters: value})
  })
document.getElementById("search").focus();
</script>


<div id=mainmatter>
<h4>Filme</h4><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/17083.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=17083&listId=287">Soul</a> &nbsp; 2020</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/18825.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=18825&listId=287">Der Seelenfänger</a> (Le mangeur d'âmes / The Soul Eater)  &nbsp; 2024</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/15780.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=15780&listId=287">Körper und Seele</a> (Teströl és lélekröl / On Body and Soul)  &nbsp; 2017</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/12897.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=12897&listId=287">Soul Boy</a> &nbsp; 2010</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/12365.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=12365&listId=287">Soul Kitchen</a> &nbsp; 2009</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/12107.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=12107&listId=287">Soul Power</a> &nbsp; 2008</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/10437.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=10437&listId=287">Island of Lost Souls</a> (De Fortabte sjæles ø)  &nbsp; 2007</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/10269.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=10269&listId=287">Als der Wind den Sand berührte</a> (Si le vent souleve les sables)  &nbsp; 2006</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/8189.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=8189&listId=287">The Soul of a Man</a> (The Blues)  &nbsp; 2003</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/11251.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=11251&listId=287">Terry Pratchetts Discworld: Soul Music</a> (Soul Music)  &nbsp; 1997</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/9078.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=9078&listId=287">Angst essen Seele auf</a> (Ali: Fear Eats The Soul)  &nbsp; 1974</p><p class=filmshort><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/9015.jpg');" onmouseout="change_mouse('');"  href="/cgi-bin/film5.pl?filmId=9015&listId=287">Tanz der toten Seelen</a> (Carnival of Souls)  &nbsp; 1962</p><h4>Personen</h4><p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=45869">Soultanakis, Nico </a> &nbsp; (Drehbuch / <a href="film5.pl?filmId=11627">The Fall</a>)</<p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=23472">Soul, David </a> &nbsp; (Nebenrolle / <a href="film5.pl?filmId=10559">Rendezvous mit einer Leiche</a>, <a href="film5.pl?filmId=8602">Starsky & Hutch</a>, <a href="film5.pl?filmId=7873">Calahan - Dirty Harry 2</a>...)</<p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=46672">Soulis, Anastasios </a> &nbsp; (Nebenrolle / <a href="film5.pl?filmId=11796">Wir sind alle erwachsen</a>)</<p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=82840">Souley Maiga, Balkissa </a> &nbsp; (Nebenrolle / <a href="film5.pl?filmId=18926">Konklave</a>)</<p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=59296">Soul, Zoë </a> &nbsp; (Nebenrolle / <a href="film5.pl?filmId=14515">The Purge: Anarchy</a>)</<p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=62825">Soulwax,  </a> &nbsp; (Musik / <a href="film5.pl?filmId=15229">Café Belgica</a>)</<p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=43500">Koli, Souleyman </a> &nbsp; (Hauptrolle / <a href="film5.pl?filmId=11124">Sirga - Die Löwin</a>)</<p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=52908">Soulanes, Louis </a> &nbsp; (Kamera / <a href="film5.pl?filmId=13232">La Pointe Courte</a>)</<p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=52910">Soulignac, Paul </a> &nbsp; (Kamera / <a href="film5.pl?filmId=13232">La Pointe Courte</a>)</<p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=66913">Ndiaye, Souleymane Seye </a> &nbsp; (Nebenrolle / <a href="film5.pl?filmId=16115">Bonjour Paris</a>)</<p class=filmshort><p class="filmshort"><a href="suchen5.pl?personId=74403">Sylla, Souleymane </a> &nbsp; (Nebenrolle / <a href="film5.pl?filmId=17326">Tolo Tolo - Die große Reise</a>)</
</div>


<p style="margin-bottom:32px;font-size:15px"><h3>Suchergebnis</h3></p>
<p style="margin-bottom:1ex"><b>Heute</b> vor 39 Jahren wurde <a href="/cgi-bin/suchen5.pl?personId=33832">Elliot Page</a> geboren.</p><center></center>

<div id="MM" style="position:absolute;">
<img style="-moz-opacity:0.6" id="MMBILD" src="/png/preview.png" height="160">
</div>

<script>


if (navigator.appName.indexOf("Microsoft")!=-1) {
 } else {
   document.getElementById("MMBILD").MozOpacity=0.6;
}

Browser="";
if (navigator.appName.indexOf("Netscape")!=-1) {
  if (document.layers)
     Browser="NS4"
  else
     Browser="NS6"
}
if (document.all)
   Browser="IE";


function mouse_moved(e) {
  if(Browser=="NS4") {
    x=e.pageX;
    y=e.pageY;
    document.MM.top=y+15;
    document.MM.left=x+15;
  }
  else if(Browser=="NS6") {
     x=e.pageX;
     y=e.pageY;
     document.getElementById("MM").style.top=y-175 + "px";
     document.getElementById("MM").style.left=x+15 + "px";
  }
  else if(Browser=="IE") {
    x =document.body.scrollLeft+event.clientX;
    y =document.body.scrollTop+event.clientY;
    document.all.MM.style.top=y+5;
    document.all.MM.style.left=x+5;
  }
}

if(Browser=="NS4"||Browser=="NS6") {
  document.captureEvents(Event.MOUSEMOVE);
}

document.onmousemove = mouse_moved;

function change_mouse(src) {
  if (src=="") 
     src="/png/preview.png";
  if(Browser=="IE")
    document.images["MMBILD"].src=src;
  else if(Browser=="NS4")
    document.MM.document.images[0].src=src;
  else if(Browser=="NS6") {
     document.getElementById("MMBILD").src=src;
     document.getElementById("MMBILD").MozOpacity=0.6;
     document.getElementById("MM").MozOpacity=0.6;
  }
}
</script>

  </div></div>

  <footer>
    <div id="footer5"></div>
  </footer>

</body>
</html>
"""

@pytest.fixture
def film_html():
    """Film page source html of first film result in search_html ("Soul (2020)")"""
    # removed comments in source html
    return """
<!DOCTYPE html>
<html><head>
<link rel="stylesheet" href="/css/iv5.css" type="text/css">
<link rel="SHORTCUT ICON" href="https://www.filmgalerie-phaseiv.de/png/AmeiseWeb_hgTransp_300px.png">

<title> Soul </title>
  <script type="text/javascript" src="/js/navigator5.js"></script>
  <script type="text/javascript" src="/js/footer5.js"></script>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="Author" content="DB+GNU Emacs+w3schools">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link rel="stylesheet" href="/notfall.css" type="text/css"></head>

<body onload="navigator5(); footer5();"> <img class="notfall" src="/png/notfall.png" />

  <nav>
    <div id="navigator5"></div>
  </nav>

  <div class="main">

    <table cellspacing=0 width='100%'><col width='20%'><col width='80%'><tr><td></td><td><p style='margin-bottom: 30px; height: 60px;'><span class='filmtitel'>Soul</span><br>  <a href="stoebern5.pl?l=3">USA</a> &nbsp;&nbsp;  2020 &nbsp;&nbsp;96 &nbsp;min &nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;<br>&nbsp;</p></td></tr><tr><td style='border-bottom: 1px solid;'>Standort&nbsp;</td><td align=center style='border-bottom: 1px solid; padding: 15px;'><b>Kinderfilm - Animation</b></td></tr><tr><td style='border-bottom: 1px solid;'>Status&nbsp;</td><td align=center style='border-bottom: 1px solid; padding: 15px'><b style='color: #3cb371;'>verf&uuml;gbar</b></td></tr><tr><td style='border-bottom: 1px solid;'>Liste navigieren</td><td align=center style='border-bottom: 1px solid; padding: 15px'><img src='/png/arrow_ende.png' width=20px style='margin-bottom:-5px'>&nbsp;<span style='color: #e36656; font-weight:bold;'> Soul </span> &nbsp;<a accesskey=X href="film5.pl?filmId=18825&listId=286">&nbsp;<img src='/png/arrow_right.png' width=20px style='margin-bottom:-5px'></a></td></tr><tr><td valign=top style='height: 20px;'>&nbsp;</td><td>&nbsp;</td></tr></table>

    <p class="smallskip"> <img src="https://www.phase-iv.de/images//filme/17083.jpg" valign="top" align="right" class="image35vw" alt=""> Joe Gardner (Stimme:<a href="/cgi-bin/suchen5.pl?personId=15618">Jamie Foxx</a>) ist Musiklehrer an einer Schule in New York. Sein größter Wunsch ist es jedoch, als Jazz-Musiker groß rauszukommen und das Unterrichten endlich an den Nagel hängen zu können. Als sich ihm eines Tages die langersehnte Gelegenheit bietet, mit der berühmten Jazz-Saxophonistin Dorothea (Stimme:<a href="/cgi-bin/suchen5.pl?personId=1411">Angela Bassett</a>) aufzutreten, baut Joe einen Unfall – und seine Seele landet an einem Ort im "Davorseits". Dort werden ungeborene Seelen mit ihren Persönlichkeiten ausgestattet und auf das Leben auf der Erde vorbereitet. Joe setzt alles daran, um wieder in seinen Körper auf der Erde zu gelangen, denn seinen Auftritt will er um nichts in der Welt verpassen. Dafür tut sich der leidenschaftliche Musiker mit der abgeklärten Seele 22 (<a href="/cgi-bin/suchen5.pl?personId=36792">Tina Fey</a>) zusammen, die schon ewig im "Davorseits" hockt und keine Lust auf ein Dasein auf der Erde hat. Sie verspricht, Joe zu helfen und beginnt dabei langsam zu begreifen, dass das Leben vielleicht doch mehr Schönes zu bieten hat, als sie bisher dachte...
<p class="smallskip">Die Kinderfilme Pixars bieten zumeist einige Aspekte die auch den Erwachsenen gefallen, im Falle von "Soul" scheint es aber (nicht zum ersten Mal, siehe z.B. "<a href="/cgi-bin/film5.pl?filmId=14918">Alles steht Kopf</a>") andersherum zu sein: Ein Film primär für die Erwachsenen mit lustigen Momenten für die Jüngeren obendrauf. Wie der Großteil des Pixar-Katalogs eine klare Empfehlung. <ul></ul></p>

    <table cellspacing=0 width='100%'><tr><td valign=top>Genre&nbsp;</td><td> <a href="stoebern5.pl?g=18">Abenteuerfilm</a>&nbsp;&nbsp; <a href="stoebern5.pl?g=5">Animationsfilm</a>&nbsp;&nbsp; <a href="stoebern5.pl?g=1">Komödie</a>&nbsp;&nbsp; <a href="stoebern5.pl?g=9">Musikfilm</a>&nbsp;&nbsp; <a href="stoebern5.pl?g=14">Fantasy</a>&nbsp;&nbsp; <a href="stoebern5.pl?g=11">Kinderfilm</a></td></tr><tr><td valign=top>Stichwort&nbsp;</td><td> <a href="stoebern5.pl?stw=119">Jazz</a>&nbsp;&nbsp; <a href="stoebern5.pl?stw=213">Pixar</a>&nbsp;&nbsp; <a href="stoebern5.pl?stw=104">New York</a></td></tr><tr><td valign=top>Awards&nbsp;</td><td> <a href="stoebern5.pl?a=59">Oscar: Bester Animationsfilm</a>  f&uuml;r Dana Murray, Pete Docter<br><a href="stoebern5.pl?a=96">Oscar: Beste Filmmusik</a>  f&uuml;r Trent Reznor, Kemp Powers</td></tr><tr><td valign=top>Sprachen&nbsp;</td><td> <a href="stoebern5.pl?s=1">Deutsch</a>&nbsp;&nbsp; <a href="stoebern5.pl?s=2">Englisch</a>&nbsp;&nbsp;&nbsp;</td></tr><tr><td valign=top>Untertitel&nbsp;</td><td> <a href="stoebern5.pl?u=1">Deutsch</a>&nbsp;&nbsp; <a href="stoebern5.pl?u=2">Englisch</a>&nbsp;&nbsp;&nbsp;</td></tr><tr><td valign=top>&nbsp;</td><td>&nbsp;</td></tr><tr><td valign=top>Regie&nbsp;</td><td><a href="/cgi-bin/suchen5.pl?personId=30139">Pete&nbsp;Docter</a> &nbsp;&nbsp;  <a href="/cgi-bin/suchen5.pl?personId=72726">Kemp&nbsp;Powers</a> &nbsp;&nbsp;   </td></tr><tr><td valign=top>Drehbuch&nbsp;</td><td><a href="/cgi-bin/suchen5.pl?personId=30139">Pete&nbsp;Docter</a> &nbsp;&nbsp;  <a href="/cgi-bin/suchen5.pl?personId=72727">Mike&nbsp;Jones</a> &nbsp;&nbsp;  <a href="/cgi-bin/suchen5.pl?personId=72726">Kemp&nbsp;Powers</a> &nbsp;&nbsp;   </td></tr><tr><td valign=top>Hauptrolle&nbsp;</td><td><a href="/cgi-bin/suchen5.pl?personId=15618">Jamie&nbsp;Foxx</a> &nbsp;&nbsp;  <a href="/cgi-bin/suchen5.pl?personId=36792">Tina&nbsp;Fey</a> &nbsp;&nbsp;   </td></tr><tr><td valign=top>Nebenrolle&nbsp;</td><td><a href="/cgi-bin/suchen5.pl?personId=41073">Alice&nbsp;Braga</a> &nbsp;&nbsp;  <a href="/cgi-bin/suchen5.pl?personId=63936">Rachel&nbsp;House</a> &nbsp;&nbsp;  <a href="/cgi-bin/suchen5.pl?personId=52971">Richard&nbsp;Ayoade</a> &nbsp;&nbsp;  Graham&nbsp;Norton &nbsp;&nbsp;   </td></tr><tr><td valign=top>Kamera&nbsp;</td><td><a href="/cgi-bin/suchen5.pl?personId=65892">Matt&nbsp;Aspbury</a> &nbsp;&nbsp;  <a href="/cgi-bin/suchen5.pl?personId=72731">Ian&nbsp;Megibben</a> &nbsp;&nbsp;   </td></tr><tr><td valign=top>Musik&nbsp;</td><td><a href="/cgi-bin/suchen5.pl?personId=48977">Atticus&nbsp;Ross</a> &nbsp;&nbsp;  <a href="/cgi-bin/suchen5.pl?personId=50434">Trent&nbsp;Reznor</a> &nbsp;&nbsp;   </td></tr><tr><td valign=top>Produzent&nbsp;</td><td>Dana&nbsp;Murray &nbsp;&nbsp;   </td></tr><tr><td valign=top>Schnitt&nbsp;</td><td>Kevin &nbsp;Nolting &nbsp;&nbsp;  </td></tr><tr><td valign=top><br>Kunden, die <br>diesen Film <br>ausgeliehen haben, <br>liehen auch:</td><td><br> <p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/15081.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=15081">Zoomania</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/8881.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=8881">Fluch der Karibik 2</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/15454.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=15454">Phantastische Tierwesen und wo sie zu finden sind</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/2083.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=2083">Harry Potter und der Stein der Weisen</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/3812.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=3812">Fluch der Karibik</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/15504.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=15504">Vaiana - Das Paradies hat einen Haken</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/16210.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=16210">Phantastische Tierwesen: Grindelwalds Verbrechen</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/10031.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=10031">Fluch der Karibik 3</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/2942.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=2942">Harry Potter und die Kammer des Schreckens</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/14772.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=14772">Marvel's The Avengers 2 - Age of Ultron</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/14535.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=14535">Guardians of the Galaxy</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/1272.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=1272">Star Wars Episode 1 - Die dunkle Bedrohung</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/12807.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=12807">Rapunzel - Neu verföhnt</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/12990.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=12990">Rio</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/13588.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=13588">Merida - Legende der Highlands</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/16132.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=16132">Die Unglaublichen 2</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/17130.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=17130">Raya und der letzte Drache</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/16394.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=16394">Pets 2</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/14918.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=14918">Alles steht Kopf</a></p><p class='filmshort2'><a onmouseover="change_mouse('https://www.phase-iv.de/images/filme/9936.jpg');" onmouseout="change_mouse('');" href="/cgi-bin/film5.pl?filmId=9936">Hände weg von Mississippi</a></p><div id="MM" style="position:absolute;">
<img style="-moz-opacity:0.6" id="MMBILD" src="/png/preview.png" height="160">
</div>

<script>

if (navigator.appName.indexOf("Microsoft")!=-1) {
 } else {
   document.getElementById("MMBILD").MozOpacity=0.6;
}

Browser="";
if (navigator.appName.indexOf("Netscape")!=-1) {
  if (document.layers)
     Browser="NS4"
  else
     Browser="NS6"
}
if (document.all)
   Browser="IE";


function mouse_moved(e) {
  if(Browser=="NS4") {
    x=e.pageX;
    y=e.pageY;
    document.MM.top=y+15;
    document.MM.left=x+15;
  }
  else if(Browser=="NS6") {
     x=e.pageX;
     y=e.pageY;
     document.getElementById("MM").style.top=y-175 + "px";
     document.getElementById("MM").style.left=x+15 + "px";
  }
  else if(Browser=="IE") {
    x =document.body.scrollLeft+event.clientX;
    y =document.body.scrollTop+event.clientY;
    document.all.MM.style.top=y+5;
    document.all.MM.style.left=x+5;
  }
}

if(Browser=="NS4"||Browser=="NS6") {
  document.captureEvents(Event.MOUSEMOVE);
}

document.onmousemove = mouse_moved;

function change_mouse(src) {
  if (src=="") 
     src="/png/preview.png";
  if(Browser=="IE")
    document.images["MMBILD"].src=src;
  else if(Browser=="NS4")
    document.MM.document.images[0].src=src;
  else if(Browser=="NS6") {
     document.getElementById("MMBILD").src=src;
     document.getElementById("MMBILD").MozOpacity=0.6;
     document.getElementById("MM").MozOpacity=0.6;
  }
}
</script>
</td></tr></table>

  </div>

  <footer>
    <div id="footer5"></div>
  </footer>

</body>
</html>
"""

@pytest.fixture
def film_unavailable_html(film_html):
    """Same as `film_html` but with Film.Status.available = False as expected output."""
    return film_html.replace("verf&uuml;gbar", "ausgeliehen")

@pytest.fixture
def search_list_id():
    """Expected list_id result from parsing search_html"""
    return 287

@pytest.fixture
def search_num_results():
    """Expected number of search result items from parsing search_html"""
    return 12

@pytest.fixture
def film():
    """Expected Film item result from parsing FILM_HTML and first search result in SEARCH_HTML"""
    return Film(
        filmID=17083,
        title='Soul',
        alternative_titles=[],
        year=2020,
        image_url='https://www.phase-iv.de/images//filme/17083.jpg',
        film_url='https://www.filmgalerie-phaseiv.de/cgi-bin/film5.pl?filmId=17083',
        status=Status(available=True, location='Kinderfilm - Animation'),
        director=['Pete Docter', 'Kemp Powers'],
        screenplay=['Pete Docter', 'Mike Jones', 'Kemp Powers'],
        main_cast=['Jamie Foxx', 'Tina Fey'],
        supporting_cast=['Alice Braga', 'Rachel House', 'Richard Ayoade'],
        cinematographer=['Matt Aspbury', 'Ian Megibben'],
        composer=['Atticus Ross', 'Trent Reznor'],
        producers=['Dana Murray'],
        genres=['Abenteuerfilm', 'Animationsfilm', 'Komödie', 'Musikfilm', 'Fantasy', 'Kinderfilm'],
        keywords=['Jazz', 'Pixar', 'New York'],
        languages=['Deutsch', 'Englisch'],
        subtitles=['Deutsch', 'Englisch'],
        description='''Joe Gardner (Stimme: Jamie Foxx ) ist Musiklehrer an einer Schule in New York. Sein größter '''
            '''Wunsch ist es jedoch, als Jazz-Musiker groß rauszukommen und das Unterrichten endlich an den Nagel '''
            '''hängen zu können. Als sich ihm eines Tages die langersehnte Gelegenheit bietet, mit der berühmten '''
            '''Jazz-Saxophonistin Dorothea (Stimme: Angela Bassett ) aufzutreten, baut Joe einen Unfall – und seine '''
            '''Seele landet an einem Ort im "Davorseits". Dort werden ungeborene Seelen mit ihren Persönlichkeiten '''
            '''ausgestattet und auf das Leben auf der Erde vorbereitet. Joe setzt alles daran, um wieder in seinen '''
            '''Körper auf der Erde zu gelangen, denn seinen Auftritt will er um nichts in der Welt verpassen. Dafür '''
            '''tut sich der leidenschaftliche Musiker mit der abgeklärten Seele 22 ( Tina Fey ) zusammen, die schon '''
            '''ewig im "Davorseits" hockt und keine Lust auf ein Dasein auf der Erde hat. Sie verspricht, Joe zu helfen '''
            '''und beginnt dabei langsam zu begreifen, dass das Leben vielleicht doch mehr Schönes zu bieten hat, als '''
            '''sie bisher dachte... Die Kinderfilme Pixars bieten zumeist einige Aspekte die auch den Erwachsenen '''
            '''gefallen, im Falle von "Soul" scheint es aber (nicht zum ersten Mal, siehe z.B. " Alles steht Kopf ") '''
            '''andersherum zu sein: Ein Film primär für die Erwachsenen mit lustigen Momenten für die Jüngeren '''
            '''obendrauf. Wie der Großteil des Pixar-Katalogs eine klare Empfehlung.'''
    )


@pytest.fixture
def no_cache_client():
    """Client with caching disabled for fast, isolated tests."""
    client = PhaseivClient(cache_enabled=False)
    return client