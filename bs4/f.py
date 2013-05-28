h="""<body> $$$$$$$$$$$$$$
<!–[if lte IE 6]>
<script type="text/javascript">
try{
document.execCommand("BackgroundImageCache", false, true);
}catch(e){}
</script>
<![endif]–> ############## </body>"""

i="""<body> $$$$$$$$$$$$$$
<!-[if lte IE 6]>
<script type="text/javascript">
try{
document.execCommand("BackgroundImageCache", false, true);
}catch(e){}
</script>
<![endif]-> ############## </body>"""


from diagnose import diagnose
diagnose(h)
