# Notices

<!-- TOC START min:1 max:3 link:true update:true -->
- [Notices](#notices)
  - [bricodash](#bricodash)
  - [Software](#software)
    - [LICENSE.md](#licensemd)
    - [sysd/app.py](#sysdapppy)
    - [html/util/camera.php](#htmlutilcameraphp)
    - [html/js/clock.js](#htmljsclockjs)
    - [jobs/vend/memoize.py](#jobsvendmemoizepy)
  - [APIs](#apis)
    - [jobs/brico/weather/open.py](#jobsbricoweatheropenpy)
    - [jobs/slack.py](#jobsslackpy)
    - [jobs/events.py, jobs/photo.py, jobs/upmeet.py](#jobseventspy-jobsphotopy-jobsupmeetpy)
    - [jobs/brite.py](#jobsbritepy)
    - [jobs/wiki.py](#jobswikipy)
    - [jobs/common/short.py](#jobscommonshortpy)
  - [Assets](#assets)
    - [img/fog.png](#imgfogpng)
    - [html/prox/mta](#htmlproxmta)
    - [html/img/flickr_nalends_super_pop.png](#htmlimgflickr_nalends_super_poppng)
    - [html/css/font](#htmlcssfont)
    - [html/img](#htmlimg)

<!-- TOC END -->


## bricodash

Bricodash copyright © 2018 Beads Land-Trujillo, except where noticed below.
Based on Hack Manhattan's defaultcast project.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact info:
* @beadsland@hackmanhattan.slack.com
* @beadsland@mastodon.social
* @beadsland@twitter.com


## Software

### LICENSE.md

Converted to markdown by Andreas Renberg.
https://github.com/IQAndreas/markdown-licenses

If there is any inconsistency between the markdown formatted license and
the license it represents, please refer to the original license for the
correct wording.

GNU Affero General Public License (AGPL) v3.0
<http://www.gnu.org/licenses/agpl-3.0.txt>.

Please read the licenses ahead of time to make sure they are correct,
and use them at your own risk. Although we have strived to keep the license
wording identical to the originals, we are not responsible for any legal
implications caused by discrepancies in the licenses.


### sysd/app.py

Based on <https://github.com/madmod/dashcast-docker>.
Copyright © 2017 John Wells. Used and adapted in good faith.
Adapted for hackmanhattan/defaultcast by @mz@hackmanhattan.slack.com, 2017.


### html/util/camera.php

Adapted from <https://github.com/simonwalz/php-mjpeg-proxy>.
Copyright © 2017 Simon Walz. Used under MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


### html/js/clock.js

Copyright © Tushar Gupta, via <https://stackoverflow.com/a/18229123>.
Used under Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0).
https://creativecommons.org/licenses/by-sa/3.0/

You do not have to comply with the license for elements of the material
in the public domain or where your use is permitted by an applicable
exception or limitation.

No warranties are given. The license may not give you all of the permissions
necessary for your intended use. For example, other rights such as publicity,
privacy, or moral rights may limit how you use the material.


### jobs/vend/memoize.py

Copyright (c) ~2017 by unknown wiki contributor, via
<https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize>.
Used under GNU General Public License, version 2 (short: GNU GPLv2 or simply
GPLv2). http://www.gnu.org/licenses/gpl-2.0.html

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


## APIs

### jobs/brico/weather/open.py

OpenWeather API used under Attribution-ShareAlike 4.0 International
(CC BY-SA 4.0). https://creativecommons.org/licenses/by-sa/4.0/

You do not have to comply with the license for elements of the
material in the public domain or where your use is permitted by
an applicable exception or limitation.

No warranties are given. The license may not give you all of the
permissions necessary for your intended use. For example, other
rights such as publicity, privacy, or moral rights may limit how
you use the material.

OpenWeather data is made available under the Open Database License:
<http://opendatacommons.org/licenses/odbl/1.0/>.
Any rights in individual contents of the database are licensed under
the Database Contents License: <http://opendatacommons.org/licenses/dbcl/1.0/>.


### jobs/slack.py

Slack Web API used under Slack's API Terms of Service.
https://slack.com/terms-of-service/api

The API is used to serve on-site dashboards,
and is not offered for use outside of our organization.

For Slack's privacy policy, see: <https://slack.com/privacy-policy>

The Slack name and logo are trademarks of Slack Technologies, Inc.


### jobs/events.py, jobs/photo.py, jobs/upmeet.py

Meetup API used under Meetup's Terms of Service and Meetup API License Guidelines.
https://help.meetup.com/hc/en-us/articles/360001636711-Meetup-API-License-Guidelines

This application uses the Meetup API but is not verified by Meetup, Inc.

For Meetup's privacy policy, see: <https://www.meetup.com/privacy/>.

The Meetup logo is a trademark of Meetup, Inc.


### jobs/brite.py

Eventbrite API used under Eventbrite's API Terms of Service.
https://www.eventbrite.com/support/articles/en_US/Troubleshooting/eventbrite-api-terms-of-use

This application is not owned, developed or controlled by Eventbrite.

For Eventbrite's privacy policy, see:
<https://www.eventbrite.com/support/articles/en_US/Troubleshooting/eventbrite-privacy-policy?lg=en_US>.


### jobs/wiki.py

#### Mediawiki

Mediawiki's API used in accordance with draft Mediawiki's API:Licensing guidelines.
https://www.mediawiki.org/wiki/API:Licensing

Content from wiki.hackmanhattan.com is the property of Hack Manhattan.

##### Logo

Mediawiki logo variant copyright © 2003 by
<https://commons.wikimedia.org/wiki/User:Anthere>.

Used under Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0) license.
https://creativecommons.org/licenses/by-sa/3.0/

You do not have to comply with the license for elements of the material in
the public domain or where your use is permitted by an applicable exception
or limitation.

No warranties are given. The license may not give you all of the permissions
necessary for your intended use. For example, other rights such as publicity,
privacy, or moral rights may limit how you use the material.


#### Github

Github's API used under Github's Terms of Service.
https://help.github.com/articles/github-terms-of-service/

For Github's privacy statement, see:
https://help.github.com/articles/github-privacy-statement/

The Github mark is a trademark of Github, Inc.


### jobs/common/short.py

Firebase Dynamic Links API used under the applicable Terms of Service
for Firebase Services. https://firebase.google.com/terms/


## Assets

### img/fog.png

Fog/mist glyph copyright © 2016 Emoji One.
Used under Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license.
https://creativecommons.org/licenses/by-sa/4.0/

You do not have to comply with the license for elements of the material
in the public domain or where your use is permitted by an applicable
exception or limitation.

No warranties are given. The license may not give you all of the permissions
necessary for your intended use. For example, other rights such as publicity,
privacy, or moral rights may limit how you use the material.

Obtained via Wikimedia Commons
<https://commons.wikimedia.org/wiki/File:Emojione_1F32B.svg>.
For an archive of Emoji One open source glyphs prior to v. 3.0, see
<https://github.com/EmojiTwo/emojitwo>.


### html/prox/mta

MTA Service Status widget proxied from
<http://www.mta.info/mta-service-status-widget>.  
Widget munged for non-interactive use and for polling without memory leaks.

The MTA logo and subway line icons are registered trademarks of the
Metropolitan Transportation Authority (MTA) [New York], and are used only
as provided within the MTA's Service Status widget.

Use of these names, logos, icons and brands does not imply endorsement.


### html/img/flickr_nalends_super_pop.png

Super Pop B-Pop <https://www.flickr.com/photos/130475615@N06/17177586749>
copyright © 2015 nalends @ Flickr. Transparency added.
Used under a Attribution-NoDerivs 2.0 Generic (CC BY-ND 2.0) license
<https://creativecommons.org/licenses/by-nd/2.0/>.

You do not have to comply with the license for elements of the material
in the public domain or where your use is permitted by an applicable
exception or limitation. No warranties are given. The license may not give
you all of the permissions necessary for your intended use. For example,
other rights such as publicity, privacy, or moral rights may limit how
you use the material.


### html/css/font

Lato copyright © 2010-2014 by tyPoland Lukasz Dziedzic (team@latofonts.com).
This Font Software is licensed under the SIL Open Font License, Version 1.1.
http://scripts.sil.org/OFL

Merriweather copyright © 2016 The Merriweather Project Authors
https://github.com/EbenSorkin/Merriweather.
This Font Software is licensed under the SIL Open Font License, Version 1.1.
http://scripts.sil.org/OFL

Noto is a trademark of Google Inc. Copyright © 2012 Google Inc.
Noto fonts are open source.
All Noto fonts are published under the SIL Open Font License, Version 1.1.
http://scripts.sil.org/OFL

Raleway copyright © 2010, Matt McInerney (matt@pixelspread.com),
Copyright (c) 2011, Pablo Impallari (www.impallari.com|impallari@gmail.com),
Copyright (c) 2011, Rodrigo Fuenzalida (www.rfuenzalida.com|hello@rfuenzalida.com).
This Font Software is licensed under the SIL Open Font License, Version 1.1.
http://scripts.sil.org/OFL


### html/img

The Hack Manhattan logo and gear icon are trademarks of Hack Manhattan, Inc.

The Fixers Collective logo is a trademark of the Fixers' Collective.

The freeCodeCamp logo and glyph are trademarks of freeCodeCamp.

All product names, logos, brands, emoji glyphs, memes and other images are
property of their respective owners. All company, product and service
identifiers used in this application are for identification purposes only.
Use of any such names, logos, and brands does not imply endorsement.
