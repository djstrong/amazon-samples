#-*- coding: utf-8 -*-

import sys
import urllib2
import re
import eyeD3
import os

if __name__ == "__main__":
  if len(sys.argv)!=2:
    sys.exit("provide link as argument")
  
  link = sys.argv[1]
  response = urllib2.urlopen(link)
  html = response.read()
  
  m3us = re.findall('"(\/gp\/dmusic\/media\/sample\.m3u.*?)"', html)
  
  if not m3us:
    sys.exit("no m3us")
    
  for i, m3u in enumerate(m3us):
    link_m3u = 'http://www.amazon.com'+m3u

    response = urllib2.urlopen(link_m3u)
    link_mp3 = response.read().strip()
    
    response = urllib2.urlopen(link_mp3)
    mp3 = response.read()
    
    f = open('temp.mp3', 'w')
    f.write(mp3)
    f.close()
    
    tag = eyeD3.Tag()
    tag.link('temp.mp3')
    
    catalog = tag.getAlbum().replace('/', ' ')
    if not os.path.exists(catalog):
      os.makedirs(catalog)
    name = catalog + '/' + tag.getArtist().replace('/', ' ') + ' - ' + tag.getTitle().replace('/', ' ')
    print i, name
    os.rename('temp.mp3', name+'.mp3')