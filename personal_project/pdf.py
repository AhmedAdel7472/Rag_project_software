from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ─── Raw product data ────────────────────────────────────────────────────────
raw = """
Recycled Materials | Chelsea F.C. Academy Pro SE Older Kids' Nike Dri-FIT Football Pre-Match Short-Sleeve Top | £49.99
F.C. Barcelona Swoosh Men's Nike Football T-Shirt | £19.99
Recycled Materials | Tottenham Hotspur 2025/26 Match Away Men's Nike Dri-FIT ADV Football Authentic Shirt | £124.99
Nike Phantom 6 Low Academy Indoor Court Football Shoes | £79.99
Recycled Materials | Inter Milan 2025/26 Match Third Men's Nike Dri-FIT ADV Total 90 Football Authentic Shirt | £124.99
Paris Saint-Germain Men's Nike Total 90 Football T-Shirt | £27.99
Recycled Materials | Nike Dri-FIT Park 3 Women's Knit Football Shorts | £16.99
Recycled Materials | Paris Saint-Germain Academy Pro Older Kids' Nike Dri-FIT Football Short-Sleeve Knit Top | £22.99
Paris Saint-Germain Jordan Club Cap | £29.99
Recycled Materials | FC Barcelona 2025/26 Stadium Fourth Women's Nike Dri-FIT Football Replica Shirt | £84.99
Bestseller | F.C. Barcelona Academy Pro Fourth Older Kids' Nike Dri-FIT Football Pre-Match Top | £49.99
Recycled Materials | Croatia 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £69.99
Recycled Materials | Chelsea F.C. 2025/26 Stadium Home Women's Nike Dri-FIT Football Replica Shirt | £84.99
Recycled Materials | F.C. Barcelona Academy Pro Home Older Kids' Nike Dri-FIT Football Pre-Match Short-Sleeve Top | £49.99
Recycled Materials | FC Barcelona Away Kobe Dri-FIT Football Jacket | £79.99
Recycled Materials | F.C. Barcelona Strike Third Men's Nike Dri-FIT Total 90 Football Knit Shorts | £39.99
Paris Saint-Germain Tech Women's Nike Football Fleece Mid-Rise Joggers | £104.99
Chelsea Women's Nike Football T-Shirt | £27.99
Recycled Materials | Tottenham Hotspur 2025/26 Match Home Men's Nike Dri-FIT ADV Football Authentic Shirt | £124.99
Recycled Materials | Inter Milan PrimaLoft Skull Peak SE Men's Nike ACG Storm-FIT Football Jacket | £289.99
Recycled Materials | Tottenham Hotspur 2025/26 Stadium Third Older Kids' Nike Dri-FIT Total 90 Football Replica Shirt | £64.99
Recycled Materials | FC Barcelona Away Kobe Dri-FIT Football 6" Shorts | £44.99
Recycled Materials | England Strike Men's Nike Dri-FIT Football Knit Pants | £69.99
FFF Tech Fleece Older Kids' (Boys') Nike Football Pants | £69.99
FFF Tech Fleece Older Kids' (Boys') Nike Football Full-Zip Hoodie | £79.99
Recycled Materials | Chelsea F.C. Academy Pro Men's Nike Dri-FIT Football Pre-Match Top | £59.99
Recycled Materials | Paris Saint-Germain 2025/26 Stadium Fourth Baby/Toddler Jordan Football Replica 3-Piece Kit | £49.99
Recycled Materials | Paris Saint-Germain Strike Fourth Older Kids' Jordan Dri-FIT Football Knit Pants | £49.99
Recycled Materials | F.C. Barcelona Academy Pro Fourth Men's Nike Dri-FIT Football Pre-Match Top | £59.99
Recycled Materials | Inter Milan Strike Third Men's Nike Dri-FIT Total 90 Football Anthem Jacket | £129.99
Recycled Materials | F.C. Barcelona 2025/26 Stadium Home Men's Nike Dri-FIT Football Replica Long-Sleeve Shirt | £94.99
Sold Out | Nigeria 2026 Stadium Goalkeeper Men's Nike Dri-FIT Football Replica Short-Sleeve Shirt | £89.99
Nike Strike Women's Nike Dri-FIT Football Knit Trousers | £54.99
Recycled Materials | Nike Strike Older Kids' Dri-FIT Football Knit Drill Top | £44.99
Netherlands The Nike Polo Men's Nike Dri-FIT Football Polo | £69.99
Recycled Materials | Nigeria 2026 Stadium Home Women's Nike Dri-FIT Football Short-Sleeve Jersey | £89.99
FFF Tech Fleece Men's Nike Football Joggers | £104.99
Inter Milan Club Men's Nike Football Pullover Hoodie | £64.99
Recycled Materials | Inter Milan 2025/26 Match Away Men's Nike Dri-FIT ADV Football Authentic Shirt | £124.99
Recycled Materials | Paris Saint-Germain 2025/26 Stadium Fourth Women's Jordan Dri-FIT Football Replica Shirt | £84.99
Nike Tech Men's Dri-FIT Short-Knit Shorts | £59.99
Nike Guard Lock Elite Football Sleeves | £17.99
Recycled Materials | Paris Saint-Germain 2025/26 Stadium Fourth Men's Jordan Dri-FIT Football Replica Shorts | £44.99
Netherlands Men's Nike Football T-Shirt | £27.99
Sold Out | S.C. Corinthians 2024/25 Stadium Third Men's Nike Dri-FIT Football Replica Shirt | £84.99
Kylian Mbappe Club Fleece Older Kids' Football Shorts | £32.99
Netherlands Tech Fleece Men's Nike Football Joggers | £104.99
Recycled Materials | Nike Js Tiempo Maestro Club Indoor Court Low-Top Football Shoes | £44.99
Recycled Materials | Inter Milan Academy Pro SE Men's Nike ACG Dri-FIT Football Long-Sleeve Pre-Match Top | £69.99
Nigeria Men's Nike Football T-Shirt | £27.99
Recycled Materials | F.C. Barcelona Strike Fourth Baby/Toddler Nike Dri-FIT Football Knit Tracksuit | £49.99
Recycled Materials | Atletico Madrid 2025/26 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £64.99
Nike Academy Team Football Duffel Bag (Large, 95L) | £42.99
Recycled Materials | F.C. Barcelona Strike Fourth Older Kids' Nike Dri-FIT Football Pre-Match Drill Top | £59.99
Recycled Materials | Nike United Academy Women's Dri-FIT Football Knit Pants | £39.99
Recycled Materials | Chelsea F.C. 2024/25 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £84.99
Inter Milan Tech Men's Nike Football Fleece Shorts | £79.99
Recycled Materials | Nike Academy Older Kids' (Girls') Dri-FIT Football Shorts | £16.99
FFF Club Men's Nike Football French Terry Pullover Hoodie | £64.99
Recycled Materials | Chelsea F.C. 2025/26 Stadium Away Older Kids' Nike Dri-FIT Football Replica Shirt | £64.99
Tottenham 2025/2026 Nike Just Do It Mini Backpack | £32.99
Recycled Materials | Chelsea F.C. Academy Pro Third Older Kids' Nike Dri-FIT Total 90 Football Anthem Jacket | £64.99
Recycled Materials | Nike Total 90 Men's Dri-FIT Short-Sleeve Football Top | £59.99
Jordan Trunner O/S Women's Shoes | £99.99
F.C. Barcelona Primary Away Men's Kobe Dri-FIT Football Short-Sleeve Top | £49.99
Recycled Materials | Paris Saint-Germain Strike Fourth Older Kids' Jordan Dri-FIT Football Short-Sleeve Top | £32.99
Recycled Materials | FC Barcelona Away Kobe Therma-FIT Football Pullover Hoodie | £79.99
Nike Academy Football Gymsack (18L) | £19.99
Recycled Materials | Inter Milan Wolf Tree Plus SE Nike ACG Soccer Fleece Trousers | £134.99
Recycled Materials | Chelsea F.C. Strike Younger Kids' Nike Dri-FIT Football Knit Tracksuit | £54.99
Recycled Materials | Norway 2026 Stadium Away Men's Nike Football Dri-FIT Replica Shorts | £49.99
Recycled Materials | Brazil Strike Men's Nike Dri-FIT Football Drill Top | £69.99
Recycled Materials | Poland 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £69.99
Recycled Materials | Paris Saint-Germain Strike Night Edition Older Kids' Jordan Dri-FIT Football Knit Pants | £49.99
FFF Women's Nike Football T-Shirt | £27.99
Nike Maestro Futsal Ball | £29.99
Tottenham Hotspur 2025/26 Academy Therma-FIT Gloves | £24.99
Recycled Materials | South Korea 2004 Total 90 Reissue Men's Nike Football Replica Shirt | £84.99
Recycled Materials | F.C. Barcelona Academy Pro Home Men's Nike Dri-FIT Football Pre-Match Short-Sleeve Top | £59.99
Paris Saint-Germain Strike Windrunner PrimaLoft Fourth Men's Jordan Storm-FIT Football Hooded Jacket | £209.99
Recycled Materials | Chelsea F.C. 2025/26 Match Away Men's Nike Dri-FIT ADV Football Authentic Shirt | £124.99
Recycled Materials | Paris Saint-Germain Academy Pro Fourth Older Kids' Jordan Dri-FIT Football Pre-Match Top | £49.99
Recycled Materials | USMNT 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £69.99
Recycled Materials | F.C. Barcelona Strike SE Men's Nike Dri-FIT Football Knit Shorts | £39.99
Recycled Materials | Inter Milan 2025/26 Match Home Men's Nike Dri-FIT ADV Football Authentic Shirt | £124.99
Recycled Materials | Brazil 2026 Match Away Women's Jordan Aero-FIT Football Authentic Shirt | £134.99
Recycled Materials | Nike Academy Men's Dri-FIT Football Drill Top | £39.99
Recycled Materials | F.C. Barcelona Men's Nike Football Total 90 Football Tracksuit Jacket | £99.99
Recycled Materials | Nike Therma-FIT Academy Older Kids' Football Pants | £49.99
Recycled Materials | Nike Strike 'Alexia Putellas' Women's Dri-FIT Football Short-Sleeve Top | £37.99
Recycled Materials | Nike Academy+ Older Kids' Dri-FIT Football Shorts | £22.99
Recycled Materials | Paris Saint-Germain Strike Night Edition Men's Jordan Dri-FIT Football Knit Shorts | £39.99
Recycled Materials | F.C. Barcelona Strike Fourth Younger Kids' Nike Dri-FIT Football Knit Tracksuit | £54.99
Recycled Materials | FC Barcelona Essential Repel Women's Nike Football Woven Hooded Jacket | £74.99
Recycled Materials | Brazil 2026 Stadium Away Men's Jordan Dri-FIT Football Replica Shorts | £49.99
Nike Js Tiempo Streetgato PRM Older Kids' Indoor Court Low-Top Football Shoes | £64.99
Recycled Materials | F.C. Barcelona 2025/26 Match Third Men's Nike Dri-FIT ADV Total 90 Football Authentic Shirt | £124.99
Jordan Pro Unstructured Flat-Bill Hat | £32.99
Recycled Materials | Inter Milan Wolf Tree Plus SE Nike ACG Football Full-Zip Hoodie | £164.99
Nike Tiempo Streetgato LE Indoor Court Low-Top Football Shoes | £79.99
Nike Charge Football Shinguards | £24.99
Recycled Materials | F.C. Barcelona Strike Fourth Men's Nike Dri-FIT Football Tracksuit | £129.99
Recycled Materials | Nike Tech Men's Dri-FIT Short Knit Pants | £79.99
Recycled Materials | Netherlands 2026 Stadium Goalkeeper Men's Nike Dri-FIT Football Replica Short-Sleeve Shirt | £89.99
Recycled Materials | FFF 2026 Stadium Away Men's Nike Football Dri-FIT Replica Shorts | £49.99
Nigeria Men's Nike Football T-Shirt | £32.99
Recycled Materials | Nike United Academy Women's Dri-FIT Woven Football Tracksuit | £74.99
Recycled Materials | Inter Milan 2026 Match SE Men's Nike ACG Dri-FIT ADV Football Authentic Shirt | £124.99
Recycled Materials | Chelsea F.C. Academy Pro SE Men's Nike Dri-FIT Football Pre-Match Short-Sleeve Top | £59.99
Recycled Materials | Paris Saint-Germain Strike Night Edition Younger Kids' Jordan Dri-FIT Football Knit Tracksuit | £54.99
Bestseller | Chelsea F.C. 2025/26 Stadium Third Older Kids' Nike Dri-FIT Total 90 Football Replica Shirt | £64.99
Recycled Materials | Nike Total 90 Men's Repel Football Tracksuit Jacket | £89.99
Recycled Materials | Nike Strike 'Alexia Putellas' Women's Dri-FIT Football Shorts | £37.99
Recycled Materials | South Korea 2004 Total 90 Reissue Men's Nike Football Replica Tracksuit Bottoms | £74.99
Recycled Materials | Paris Saint-Germain Academy Pro Third Older Kids' Nike Dri-FIT Football Pre-Match Top | £49.99
Poland 2026 Stadium Home Younger Kids' Nike Football Replica 3-Piece Kit | £54.99
Recycled Materials | Nike Academy+ Men's Dri-FIT Football Shorts | £29.99
Recycled Materials | Nike Academy Women's Dri-FIT Crew-Neck Long-Sleeve Football Top | £39.99
Chelsea F.C. Club Men's Nike Football Hooded Jacket | £89.99
Nike Guard Stay 2 Football Sleeve | £11.99
Recycled Materials | Nike Tiempo Maestro Academy Multi-Ground Low-Top Football Boot | £79.99
Recycled Materials | Kylian Mbappe Older Kids' Full-Zip Woven Football Tracksuit | £69.99
Recycled Materials | Paris Saint-Germain Strike Fourth Older Kids' Jordan Dri-FIT Football Drill Top | £49.99
Recycled Materials | Paris Saint-Germain 2025/26 Stadium Third Younger Kids' Nike Dri-FIT Total 90 Football 3-Piece Kit | £54.99
Recycled Materials | Chelsea F.C. Strike SE Men's Nike Soccer Repel Woven Trousers | £79.99
Recycled Materials | Brazil Academy Pro Men's Nike Dri-FIT Football Tracksuit Bottoms | £54.99
Recycled Materials | Nike Strike Elite Men's Dri-FIT ADV Football Drill Top | £79.99
Recycled Materials | Chelsea F.C. 2025/26 Stadium Third Younger Kids' Nike Dri-FIT Total 90 Football 3-Piece Kit | £54.99
Nike Phantom 6 Low Club Indoor Court Football Shoes | £59.99
Jordan Women's Sleeveless Tank | £37.99
FFF Club Older Kids' (Boys') Nike Football Pullover Hoodie | £42.99
Recycled Materials | Inter Milan Older Kids' Nike Football Synthetic Fill Hooded Jacket | £79.99
Recycled Materials | Netherlands 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shorts | £34.99
Recycled Materials | Canada 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £64.99
Recycled Materials | Chelsea F.C. 2025/26 Stadium Home Men's Nike Dri-FIT Football Replica Long-Sleeve Shirt | £94.99
Nike Guard Lock Football Sleeves | £11.99
Recycled Materials | Paris Saint-Germain Strike Night Edition Older Kids' Jordan Dri-FIT Football Short-Sleeve Knit Top | £32.99
Netherlands Tech Fleece Windrunner Men's Nike Football Full-Zip Hoodie | £124.99
Recycled Materials | Norway 2026 Stadium Third Men's Nike Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | Paris Saint-Germain Strike Elite Night Edition Men's Jordan Aerogami Football Shell-Top | £219.99
Recycled Materials | F.C. Barcelona Strike Fourth Older Kids' Nike Dri-FIT Football Tracksuit | £89.99
Recycled Materials | Paris Saint-Germain Strike Night Edition Men's Jordan Dri-FIT Football Knit Tracksuit | £89.99
Recycled Materials | Chelsea F.C. Strike Home Nike Dri-FIT Football Knee-High Socks | £17.99
Recycled Materials | Paris Saint-Germain Tech Fleece Men's Nike Football Pants | £154.99
Recycled Materials | Paris Saint-Germain 2026 Stadium Night Edition Women's Jordan Dri-FIT Football Replica Shirt | £84.99
Recycled Materials | Brazil Academy Pro Men's Jordan Dri-FIT Football Tracksuit Bottoms | £54.99
Recycled Materials | Nike Strike Women's Dri-FIT Football Short-Sleeve Top | £37.99
Recycled Materials | Nike United Academy Older Kids' (Girls') Dri-FIT Football Short-Sleeve Top | £29.99
Paris Saint-Germain Tech Windrunner Men's Nike Football Full-Zip Woven Jacket | £124.99
Recycled Materials | Nike Academy+ Men's Dri-FIT Short-Sleeve Football Shirt | £27.99
Recycled Materials | Vini Jr. Academy Older Kids' Nike Dri-FIT Short-Sleeve Football Top | £29.99
Recycled Materials | USMNT 2026 Match Home Men's Nike Aero-FIT Football Authentic Jersey | £134.99
Jordan Women's Graphic Brazil Crew-Neck Top | £39.99
Bestseller | Nike Academy Older Kids' Therma-FIT Football Gloves | £24.99
Nike Match Goalkeeper Football Gloves | £29.99
Nike Tiempo Maestro Elite Soft-Ground Low-Top Football Boot | £239.99
Recycled Materials | Inter Milan Canwell Glacier SE Men's Nike ACG Therma-FIT ADV Football Bottoms | £164.99
Nike Js Mercurial Vapor 16 Academy Younger/Older Kids' Turf Low-Top Football Shoes | £59.99
Recycled Materials | Paris Saint-Germain 2025/26 Stadium Home Women's Nike Dri-FIT Football Replica Shirt | £84.99
Recycled Materials | Jordan Brooklyn Men's Woven Shorts | £39.99
FFF VaporFast Home Nike Dri-FIT ADV Football Knee-High Socks | £19.99
Recycled Materials | Paris Saint-Germain 2024/25 Stadium Away Younger Kids' Nike Football Replica 3-Piece Kit | £54.99
Croatia 2026 Stadium Home Younger Kids' Nike Football Replica 3-Piece Kit | £54.99
Poland 2026 Men's Nike Football T-Shirt | £27.99
Recycled Materials | F.C. Barcelona Strike Fourth Older Kids' Nike Dri-FIT Football Knit Pants | £49.99
Just In | Jordan Women's Tunnel Trousers | £79.99
Recycled Materials | Atletico Madrid 2025/26 Match Home Men's Nike Dri-FIT ADV Football Authentic Shirt | £124.99
Recycled Materials | Nike Academy+ Men's Dri-FIT Football Shorts | £27.99
Nike Phantom 6 Low Academy 'Erling Haaland' Indoor Court Football Shoes | £84.99
Recycled Materials | Poland 2026 Match Home Men's Nike Aero-FIT Football Authentic Shirt | £134.99
Recycled Materials | Nike Strike Men's Dri-FIT Football Trousers | £54.99
Recycled Materials | Paris Saint-Germain Strike Night Edition Baby/Toddler Jordan Dri-FIT Football Knit Tracksuit | £49.99
Nike Phantom 6 Low Academy Soft-ground Football Boot | £84.99
Nike Tiempo Reactgato Indoor Court Low-Top Football Shoes | £109.99
Recycled Materials | Vini Jr. Academy Older Kids' Nike Dri-FIT Football Shorts | £29.99
Nigeria Primary Men's Nike Dri-FIT Football T-Shirt | £49.99
Bestseller | Paris Saint-Germain 2025/26 Stadium Third Older Kids' Nike Dri-FIT Total 90 Football Replica Shirt | £64.99
Recycled Materials | F.C. Barcelona Strike Fourth Men's Nike Dri-FIT Football Short-Sleeve Top | £44.99
Norway Men's Nike Football T-Shirt | £27.99
Nike Tiempo Reactgato LE Indoor Court Low-Top Football Shoes | £109.99
Recycled Materials | Netherlands 2026 Stadium Home Baby/Toddler Nike Football Replica 3-Piece Kit | £54.99
Nike Victori One Men's Shower Slide | £29.99
Nike Js Tiempo Streetgato Older Kids' Indoor Court Low-Top Football Shoes | £59.99
Nike Js Mercurial Vapor 16 Club 'Vini Jr.' Older Kids' Multi-Ground Low-Top Football Boot | £49.99
Recycled Materials | Paris Saint-Germain Strike Night Edition Men's Jordan Dri-FIT Football Short-Sleeve Knit Top | £44.99
Paris Saint-Germain Tech Men's Nike Football Fleece Shorts | £79.99
Recycled Materials | Chelsea F.C. 2025/26 Match Third Men's Nike Dri-FIT ADV Total 90 Football Authentic Shirt | £124.99
Nike Js Phantom 6 High Academy Older Kids' Turf Football Shoes | £69.99
Just In | Nike Tiempo Maestro Elite LV8 Artificial-Grass Low-Top Football Boots | £239.99
Recycled Materials | Paris Saint-Germain Strike Third Men's Nike Dri-FIT Total 90 Football Knit Drill Top | £79.99
Jordan Brooklyn Fleece Men's Pullover Hoodie | £69.99
Recycled Materials | Brazil Older Kids' Nike Dri-FIT Football Pre-Match Short-Sleeve Top | £54.99
Recycled Materials | F.C. Barcelona 2025/26 Stadium Home Men's Nike Dri-FIT Football Replica Shorts | £44.99
Nike ReactX Rejuven8 Men's Slides | £54.99
Nike Phantom Dynamic Fit Football Goalkeeper Gloves | £144.99
Recycled Materials | Brazil Strike Men's Jordan Dri-FIT Football Knit Pants | £69.99
Recycled Materials | Inter Milan 2025/26 Stadium Away Men's Nike Dri-FIT Football Replica Shirt | £84.99
Recycled Materials | Nike Total 90 Men's Dri-FIT Soccer Jersey | £59.99
Nike Academy Elite Football | £59.99
Recycled Materials | Jordan Club Unstructured Hat | £24.99
Recycled Materials | Jordan Men's Polo | £59.99
Recycled Materials | Erling Haaland Academy Older Kids' Nike Dri-FIT Football Top | £29.99
Jordan Essentials Men's Mesh Jersey | £74.99
Jordan Brooklyn Women's Knit Brazil Shorts | £59.99
Recycled Materials | F.C. Barcelona 2025/26 Stadium Away Younger Kids' Kobe Football Replica 3-Piece Kit | £54.99
Nike Tiempo Streetgato Indoor Court Low-Top Football Shoes | £79.99
Nike Js Mercurial Vapor 16 Academy 'Vini Jr.' Older Kids' Indoor Court Low-Top Football Shoes | £64.99
Recycled Materials | Paris Saint-Germain Strike Night Edition Older Kids' Jordan Dri-FIT Football Knit Drill Top | £49.99
Recycled Materials | Chelsea F.C. Men's Nike Football Total 90 Football Tracksuit Jacket | £99.99
Just In | Nike Mercurial Vapor 16 Elite LV8 Artificial-Grass Low-Top Football Boots | £254.99
Turkey 2026 Fleece Men's Nike Pullover Club Hoodie | £64.99
Recycled Materials | Nike Phantom 6 Low Pro Firm-Ground Football Boot | £144.99
Recycled Materials | FFF 2026 Stadium Away Women's Nike Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | Nike Strike Men's Dri-FIT Short-Sleeve Football Top | £37.99
Bestseller | Inter Milan 2025/26 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £64.99
Men's Club Men's Nike Football Joggers | £54.99
Nike Phantom 6 Low Pro Artificial-Grass Football Boot | £144.99
Nike Academy Team Football Hard-Case Duffel Bag (Medium, 37L) | £44.99
Inter Milan SE Nike ACG Therma-FIT Football Pullover Hoodie | £114.99
Recycled Materials | Poland 2026 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £89.99
Nike Tiempo Streetgato PRM Indoor Court Low-Top Football Shoes | £79.99
Brazil Club Men's Nike Football French Terry Pullover Hoodie | £64.99
Recycled Materials | Inter Milan 2025/26 Stadium Away Younger Kids' Nike Football Replica 3-Piece Kit | £54.99
Nike Js Mercurial Vapor 16 Academy 'Kylian Mbappe' Older Kids' Artificial-Grass Low-Top Football Boots | £64.99
England Tech Fleece Older Kids' (Boys') Nike Football Pants | £69.99
Recycled Materials | Nike Strike Women's Dri-FIT Football Knit Shorts | £37.99
Nike Academy 'Vini Jr.' Football | £27.99
Kylian Mbappe Club Fleece Older Kids' Football Crew-Neck Sweatshirt | £42.99
Atletico Madrid Men's Nike Football T-Shirt | £27.99
Sold Out | Norway Tech Fleece Windrunner Men's Nike Football Full-Zip Hoodie | £124.99
Recycled Materials | Paris Saint-Germain 2025/26 Match Third Men's Nike Dri-FIT ADV Total 90 Football Authentic Shirt | £124.99
Recycled Materials | Nike Tech Men's Short-Knit Full-Zip Windrunner Jacket | £99.99
Recycled Materials | Nike Academy Older Kids' Dri-FIT Football Shorts | £22.99
Recycled Materials | England 2026 Stadium Home Women's Nike Dri-FIT Football Replica Shorts | £49.99
Recycled Materials | Tottenham Hotspur 2025/26 Stadium Away Men's Nike Dri-FIT Football Replica Shirt | £84.99
Recycled Materials | Paris Saint-Germain Strike Fourth Baby/Toddler Jordan Dri-FIT Football Knit Tracksuit | £49.99
England Older Kids' Nike Football T-Shirt | £19.99
Paris Saint-Germain Primary Third Men's Nike Dri-FIT Total 90 Football Short-Sleeve Top | £49.99
Recycled Materials | Australia 2026 Stadium Home Older Kids' Nike Dri-FIT Football Shirt | £69.99
Recycled Materials | Inter Milan Canwell Glacier SE Men's Nike ACG Therma-FIT ADV Football Jacket | £184.99
Bestseller | Paris Saint-Germain 2025/26 Stadium Fourth Older Kids' Jordan Dri-FIT Football Replica Shorts | £32.99
Bestseller | Paris Saint-Germain Strike Fourth Younger Kids' Jordan Dri-FIT Football Knit Tracksuit | £54.99
Recycled Materials | F.C. Barcelona Strike Fourth Older Kids' Nike Dri-FIT Football Short-Sleeve Top | £32.99
Recycled Materials | Nike Tiempo Maestro Academy Artificial-Grass Low-Top Football Boots | £79.99
Nike Tiempo Ligera Pro Artificial-Grass Low-Top Football Boots | £134.99
Nike Tiempo Streetgato Indoor Court Low-Top Football Shoes | £79.99
Nike Pitch Football | £19.99
Nike Academy Football Shoe Bag | £22.99
Recycled Materials | Brazil Academy Pro Older Kids' Nike Dri-FIT Football Knit Drill Top | £44.99
Recycled Materials | F.C. Barcelona Strike Fourth Older Kids' Nike Dri-FIT Football Knit Drill Top | £49.99
FFF Tech Fleece Men's Nike Football Shorts | £79.99
Recycled Materials | Nike Academy+ Men's Dri-FIT Short-Sleeve Football Shirt | £29.99
Recycled Materials | Nigeria 2026 Stadium Home Older Kids' Nike Dri-FIT Football Short-Sleeve Shirt | £69.99
Nike Academy Team Football Hardcase Duffel Bag (Large, 59L) | £49.99
Recycled Materials | Brazil 2026 Stadium Away Women's Jordan Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | Atletico Madrid 2025/26 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £84.99
Recycled Materials | Nike Dri-FIT Academy Pro Younger Kids' Knit Football Tracksuit | £42.99
Recycled Materials | Paris Saint-Germain 2026 Stadium Night Edition Men's Jordan Dri-FIT Football Replica Shorts | £44.99
FFF Tech Fleece Windrunner Men's Nike Football Full-Zip Hoodie | £124.99
Paris Saint-Germain Men's Nike Football T-Shirt | £32.99
Nike Mercurial Lite 'Kylian Mbappe' Football Shinguards | £32.99
Recycled Materials | F.C. Barcelona 2025/26 Match Away Men's Kobe Dri-FIT ADV Football Authentic Shirt | £124.99
Recycled Materials | England Strike Men's Nike Dri-FIT Football Knit Shorts | £42.99
Recycled Materials | F.C. Barcelona Academy Pro Away Older Kids' Nike Dri-FIT Football Pre-Match Short-Sleeve Top | £49.99
Erling Haaland Club Fleece Older Kids' Nike Football Crew-Neck Sweatshirt | £42.99
Recycled Materials | Paris Saint-Germain Strike Fourth Men's Jordan Dri-FIT Football Short-Sleeve Top | £44.99
Recycled Materials | FC Barcelona Away Kobe Therma-FIT Football Pants | £79.99
Recycled Materials | England 2026 Stadium Home Men's Nike Dri-FIT Football Replica Shorts | £49.99
Nike Phantom 6 Low Pro 'Erling Haaland' Firm-Ground Football Boot | £154.99
Recycled Materials | Croatia 2026 Match Home Men's Nike Aero-FIT Football Authentic Shirt | £134.99
Nike Academy Team Football Duffel Bag (Medium, 60L) | £39.99
Jordan Men's Draft Trousers | £109.99
Just In | Paris Saint-Germain 2026 Stadium Home Baby/Toddler Nike Football Replica 3-Piece Kit | £54.99
Nike Js Phantom 6 Low Academy Older Kids' Indoor Court Football Shoes | £59.99
Nike Academy "Kylian Mbappe" Football | £27.99
Recycled Materials | Turkey 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £69.99
Bestseller | Chelsea F.C. 2025/26 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £64.99
Recycled Materials | Netherlands 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £69.99
Recycled Materials | Brazil Academy Pro Older Kids' Nike Dri-FIT Football Shorts | £24.99
Paris Saint-Germain 2025/2026 Nike Academy Ball | £27.99
Jordan Men's Sleeveless Graphic T-Shirt | £37.99
Nike Mercurial Lite SuperLock Football Shinguards | £39.99
Nike Phantom 6 Low Pro 'Erling Haaland' Artificial-Grass Football Boot | £154.99
FFF Men's Nike Football T-Shirt | £32.99
Recycled Materials | USMNT 2026 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | Chelsea F.C. 2025/26 Match Home Men's Nike Dri-FIT ADV Football Authentic Shirt | £124.99
Recycled Materials | Paris Saint-Germain Strike Night Edition Men's Jordan Dri-FIT Football Knit Drill Top | £64.99
Recycled Materials | Croatia 2026 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £89.99
Nike Total 90 Premium Men's Shoes | £109.99
Nike Tiempo Maestro Academy Turf Low-Top Football Shoes | £79.99
Recycled Materials | Paris Saint-Germain 2026 Stadium Night Edition Baby/Toddler Jordan Football Replica 3-Piece Kit | £49.99
Air Jordan 85 Men's Graphic T-Shirt | £37.99
Recycled Materials | FC Barcelona 2025/26 Stadium Fourth Baby/Toddler Nike Football Replica 3-Piece Kit | £49.99
Nigeria 1996 Reissue Men's Nike Football Replica Tracksuit Jacket | £79.99
Recycled Materials | Nike Js Tiempo Maestro Club Older Kids' Turf Low-Top Football Shoes | £39.99
Nike Tiempo Reactgato Indoor Court Low-Top Football Shoes | £109.99
Recycled Materials | Inter Milan Academy Pro SE Men's Nike ACG Dri-FIT Football Short-Sleeve Pre-Match Top | £59.99
Recycled Materials | Korea 2026 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £89.99
Nike Js Phantom 6 Low Academy 'Erling Haaland' Older Kids' Indoor Court Football Shoes | £59.99
Recycled Materials | Brazil Strike Men's Nike Dri-FIT Football Knit Shorts | £42.99
Nike Js Phantom 6 Low Academy Older Kids' Turf Football Shoes | £59.99
Bestseller | F.C. Barcelona 2025/26 Stadium Third Older Kids' Nike Dri-FIT Total 90 Football Replica Shirt | £64.99
Recycled Materials | Nike Academy+ Older Kids' Dri-FIT Football Shorts | £22.99
Recycled Materials | Nike Tiempo Maestro Academy Soft-Ground Low-Top Football Boot | £79.99
Recycled Materials | Chelsea F.C. 2025/26 Stadium Away Men's Nike Dri-FIT Football Replica Shirt | £84.99
Nike Phantom Football | £22.99
Just In | Nike Phantom 6 Low Elite LV8 Artificial-Grass Football Boot | £254.99
Recycled Materials | Paris Saint-Germain 2026 Match Night Edition Older Kids' Jordan Dri-FIT ADV Football Authentic Shirt | £119.99
Recycled Materials | FC Barcelona 2025/26 Stadium Fourth Men's Nike Dri-FIT Football Replica Shirt | £84.99
Nike Js Phantom 6 High Club Older Kids' Multi-ground Football Boot | £49.99
Nike Tiempo Maestro Elite Artificial-Grass Low-Top Football Boots | £229.99
Recycled Materials | Nike Academy Women's Dri-FIT Football Shorts | £22.99
Recycled Materials | FFF Strike Men's Nike Football Dri-FIT Short-Sleeve Top | £49.99
Recycled Materials | Kylian Mbappe Academy Older Kids' Dri-FIT Short-Sleeve Football Top | £29.99
Recycled Materials | Brazil Academy Pro Men's Nike Dri-FIT Football Pre-Match Short-Sleeve Top | £64.99
Recycled Materials | F.C. Barcelona 2025/26 Stadium Third Men's Nike Dri-FIT Total 90 Football Replica Shirt | £84.99
Recycled Materials | F.C. Barcelona 2025/26 Stadium Away Men's Kobe Dri-FIT Football Replica Shirt | £84.99
Nike Phantom 6 Low Academy Artificial-Grass Football Boot | £79.99
Recycled Materials | USMNT 2026 Match Away Men's Nike Aero-FIT Football Authentic Jersey | £134.99
Recycled Materials | England Strike Men's Nike Dri-FIT Football Knit Tracksuit | £134.99
Brazil VaporFast Home Nike Dri-FIT ADV Football Knee-High Socks | £19.99
Nike Mercurial Lite Football Shinguards | £32.99
Turkey 2026 Men's Nike Football T-Shirt | £27.99
Recycled Materials | Canada 2026 Stadium Away Men's Nike Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | Brazil Strike Men's Jordan Dri-FIT Football Knit Drill Top | £69.99
Recycled Materials | Kylian Mbappe Academy Older Kids' Dri-FIT Football Shorts | £29.99
Turkey 2026 Stadium Home Younger Kids' Nike Football Replica 3-Piece Kit | £54.99
Nike Phantom 6 Low Academy EasyOn Multi-ground Football Boot | £79.99
Recycled Materials | Paris Saint-Germain 2026 Stadium Night Edition Men's Jordan Dri-FIT Football Replica Shorts | £32.99
England Hollywood Keeper Men's Nike Football Shirt | £79.99
Recycled Materials | Nike Tiempo Maestro Club Indoor Court Low-Top Football Shoes | £54.99
Nike Total 90 Men's Shoes | £99.99
Recycled Materials | Paris Saint-Germain 2026 Stadium Night Edition Men's Jordan Dri-FIT Football Long-Sleeve Replica Jersey | £94.99
Recycled Materials | Nike Academy Older Kids' Dri-FIT Football Tracksuit | £54.99
Nike Js Tiempo Maestro Academy Older Kids' Turf Low-Top Football Shoes | £59.99
Nike Dri-FIT Strike Older Kids' Short-Sleeve Football Top | £27.99
Recycled Materials | Erling Haaland Academy Older Kids' Nike Dri-FIT Football Shorts | £29.99
Recycled Materials | Nike Dri-FIT Academy Men's Dri-FIT Football Shorts | £27.99
Recycled Materials | Nike Academy Women's Dri-FIT Woven Football Tracksuit | £74.99
Recycled Materials | FC Barcelona 2025/26 Match Fourth Men's Nike Dri-FIT ADV Football Authentic Shirt | £124.99
Air Jordan 85 Men's T-Shirt | £32.99
England Club Older Kids' (Boys') Nike Football Pullover Hoodie | £42.99
Jordan Men's Goalie Top | £79.99
Recycled Materials | Chelsea F.C. Strike SE Men's Nike Football Repel Hooded Jacket | £99.99
Recycled Materials | FFF 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shorts | £34.99
Recycled Materials | England Strike Older Kids' Nike Dri-FIT Football Knit Pants | £54.99
Recycled Materials | England Older Kids' Nike Dri-FIT Football Hooded Tracksuit | £74.99
Nike Phantom 6 Low Academy Multi-ground Football Boot | £79.99
Recycled Materials | Paris Saint-Germain 2025/26 Stadium Away Men's Nike Dri-FIT Football Replica Shirt | £84.99
Recycled Materials | Nike Academy Dri-FIT Football Snood | £22.99
Recycled Materials | Australia 2026 Stadium Home Men's Nike Dri-FIT Football Shirt | £89.99
Recycled Materials | Brazil Strike Men's Nike Football Dri-FIT Short-Sleeve Top | £49.99
Recycled Materials | Chelsea F.C. 2025/26 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £84.99
Recycled Materials | Nigeria 2026 Stadium Away Men's Nike Dri-FIT Football Replica Shirt | £89.99
Nike Phantom 6 Low Club Multi-ground Football Boot | £59.99
Recycled Materials | Inter Milan 2025/26 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £84.99
Nike Tiempo Ligera Pro Turf Low-Top Football Shoes | £119.99
Just In | Paris Saint-Germain Club Men's Nike Football Polo | £39.99
Just In | Paris Saint-Germain Primary Men's Nike Dri-FIT Football T-Shirt | £49.99
Just In | Paris Saint-Germain Windrunner Home Women's Nike Football UV Woven Full-Zip Anthem Jacket | £99.99
Just In | Paris Saint-Germain Tech Windrunner Men's Nike Football Woven Full-Zip Jacket | £124.99
Nike Shox TL Men's Shoes | £154.99
Recycled Materials | Nike Js Phantom 6 Low Pro Older Kids' Multi-Ground Football Boot | £109.99
Just In | Paris Saint-Germain Windrunner Women's Nike Football UV Woven Jacket | £99.99
Just In | Paris Saint-Germain Windrunner Women's Nike Football High-Waisted Woven Pants | £89.99
Just In | Paris Saint-Germain Club Older Kids' (Boys') Nike Football Pullover Hoodie | £42.99
Just In | Paris Saint-Germain Club Fleece Older Kids' (Boys') Nike Football Joggers | £37.99
Just In | Paris Saint-Germain Club Older Kids' Nike Football T-shirt | £19.99
Just In | Paris Saint-Germain Older Kids' Nike Football T-Shirt | £19.99
Recycled Materials | Paris Saint-Germain Strike Night Edition Men's Jordan Dri-FIT Football Hooded Tracksuit | £129.99
Air Jordan Ultra Older Kids' Shoes | £84.99
Just In | Paris Saint-Germain Tech Men's Nike Football Woven Trousers | £104.99
Just In | Paris Saint-Germain Tech Fleece Men's Nike Football Shorts | £79.99
Just In | Men's Club Men's Nike Football Joggers | £54.99
Just In | Paris Saint-Germain Club Men's Nike Football Pullover Hoodie | £64.99
Bestseller | Nike Match Goalkeeper Football Gloves | £24.99
Recycled Materials | Nike Academy Team Backpack (30L) | £42.99
Recycled Materials | Nike Phantom 6 Low Pro Turf Football Shoe | £129.99
Recycled Materials | FC Barcelona 2025/26 Stadium Fourth Older Kids' Nike Dri-FIT Football Replica Shorts | £32.99
Nike Phantom 6 Low Academy 'Erling Haaland' Turf Football Shoes | £84.99
Nike Js Mercurial Vapor 16 Academy 'Kylian Mbappe' Older Kids' Turf Low-Top Football Shoes | £64.99
Nike Phantom 6 High Elite LV8 Firm-Ground Football Boot | £264.99
Nike Js Mercurial Superfly 10 Academy 'Kylian Mbappe' Older Kids' Turf High-Top Football Shoes | £74.99
Recycled Materials | Inter Milan ACG Football T-Shirt | £54.99
Recycled Materials | Turkey 2026 Match Home Men's Nike Aero-FIT Football Authentic Shirt | £134.99
Nike Phantom 6 Low Pro 'Erling Haaland' Turf Football Shoes | £134.99
England Tech Fleece Men's Nike Football Joggers | £104.99
Recycled Materials | Nike Academy Women's Dri-FIT Football Pants | £39.99
Recycled Materials | Netherlands 2026 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | Nigeria 2026 Stadium Home Men's Nike Dri-FIT Football Short-Sleeve Shirt | £89.99
Recycled Materials | Nike Strike Men's Dri-FIT Football 1/2-Zip Drill Top | £54.99
England Men's Nike Football T-Shirt | £27.99
Recycled Materials | Nike Js Tiempo Maestro Flex Younger Kids' Turf High-Top Football Boots | £39.99
Recycled Materials | Paris Saint-Germain 2025/26 Stadium Third Men's Nike Dri-FIT Total 90 Football Replica Shirt | £84.99
Nike Charge Kids' Football Shinguards | £22.99
Recycled Materials | Jordan Men's Anthem Jacket | £109.99
Nike Air Max Plus VI 'Kylian Mbappe' Men's Shoes | £174.99
Nike J Guard-CE Football Shinguards | £13.99
Recycled Materials | Netherlands 2026 Stadium Home Younger Kids' Nike Football Replica 3-Piece Kit | £54.99
Recycled Materials | Nike Dri-FIT Strike Knee-High Football Socks | £17.99
Bestseller | Paris Saint-Germain 2025/26 Stadium Fourth Younger Kids' Jordan Football Replica 3-Piece Kit | £54.99
Nike Premier 3 Turf Low-Top Football Shoes | £84.99
Nike Js Mercurial Superfly 10 Club 'Kylian Mbappe' Younger/Older Kids' Multi-Ground High-Top Football Boot | £54.99
Recycled Materials | Nike Academy Older Kids' Dri-FIT Football Knit Shorts | £16.99
Nike Premier 3 Firm-Ground Low-Top Football Boot | £99.99
Recycled Materials | Nike Academy Men's Dri-FIT Short-Sleeve Football Top | £22.99
Coming Soon | Nike Mind 002 Women's Shoes | £129.99
Bestseller | Chelsea F.C. 2025/26 Stadium Third Men's Nike Dri-FIT Football Replica Shirt | £84.99
Nike United Mercurial Superfly 10 Elite Firm-Ground High-Top Football Boot | £264.99
Nike Phantom 6 High Academy Turf Football Shoes | £84.99
Recycled Materials | Turkey 2026 Stadium Away Older Kids' Nike Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | Brazil Academy Pro Men's Jordan Dri-FIT Football Knit Shorts | £32.99
Recycled Materials | Nike Js Tiempo Maestro Academy Older Kids' Multi-Ground Low-Top Football Boot | £59.99
Nike Phantom 6 Low Academy 'Erling Haaland' Multi-ground Football Boot | £84.99
Recycled Materials | England Strike Men's Nike Dri-FIT Football Drill Top | £69.99
Recycled Materials | England Strike Older Kids' Nike Dri-FIT Football Drill Top | £54.99
Nike United Jr Phantom 6 High Academy Older Kids' Multi-Ground Football Boot | £69.99
Coming Soon | Nike Mind 002 Women's Shoes | £129.99
Recycled Materials | Brazil Academy Pro Men's Jordan Dri-FIT Football Tracksuit Jacket | £54.99
England Tech Fleece Windrunner Men's Nike Football Full-Zip Hoodie | £124.99
Nike Js Phantom 6 High Academy Older Kids' Multi-Ground Football Boot | £69.99
Nike Academy 'Erling Haaland' Football | £27.99
Nike United Mercurial Vapor 16 Academy Turf Low-Top Football Shoes | £84.99
England Women's Nike Football T-Shirt | £27.99
Recycled Materials | Brazil Academy Pro Older Kids' Nike Dri-FIT Football Short-Sleeve Knit Top | £24.99
Nike Shox R4 'Brazil' Men's Shoes | £134.99
Recycled Materials | Brazil Strike Men's Jordan Dri-FIT Football Short-Sleeve Knit Top | £49.99
Recycled Materials | NikeGrip Vapor Strike Football Crew Socks | £29.99
Recycled Materials | Brazil 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shorts | £34.99
Recycled Materials | England Strike Older Kids' Nike Dri-FIT Football Knit Shorts | £32.99
Recycled Materials | Nike Js Mercurial Vapor 16 Club Younger/Older Kids' Indoor Court Low-Top Football Shoes | £44.99
Recycled Materials | Nike Js Tiempo Maestro Club Older Kids' Multi-Ground Low-Top Football Boot | £44.99
England Club Men's Nike Football Pullover Hoodie | £64.99
Recycled Materials | Nike Strike Football Sleeves | £10.99
Recycled Materials | FFF 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £69.99
Bestseller | FC Barcelona 2025/26 Stadium Fourth Younger Kids' Nike Football Replica 3-Piece Kit | £54.99
Bestseller | Paris Saint-Germain 2025/26 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £64.99
Recycled Materials | Nike Strike Football Crew Socks | £12.99
Recycled Materials | Nigeria 1996 Reissue Men's Nike Dri-FIT Football Replica Shirt | £84.99
Recycled Materials | Paris Saint-Germain 2026 Stadium Night Edition Older Kids' Jordan Dri-FIT Football Replica Shirt | £64.99
Bestseller | FC Barcelona 2025/26 Stadium Fourth Older Kids' Nike Dri-FIT Football Replica Shirt | £64.99
Nike Sportswear 'R9' Men's T-Shirt | £37.99
Nike Air Max Plus Men's Shoes | £174.99
Nike Js Mercurial Superfly 10 Academy 'Kylian Mbappe' Younger/Older Kids' Multi-Ground High-Top Football Boot | £74.99
Recycled Materials | Nike Strike Men's Dri-FIT Football Pants | £54.99
Recycled Materials | Brazil 2026 Stadium Home Women's Nike Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | FFF 2026 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £89.99
Nike Academy Football | £24.99
Recycled Materials | Brazil 2026 Stadium Away Younger Kids' Jordan Football Replica 3-Piece Kit | £54.99
Nike Phantom 6 High Academy Multi-ground Football Boot | £84.99
Bestseller | Nike Academy Older Kids' Dri-FIT Football Pants | £32.99
Recycled Materials | Jordan Men's Diamond Shorts | £49.99
Nike Academy Over-The-Calf Football Socks | £10.99
Nike Phantom 6 High Club Multi-ground Football Boot | £64.99
Coming Soon | Nike Mind 001 Men's Pregame Mules | £79.99
Bestseller | Chelsea F.C. 2025/26 Stadium Home Younger Kids' Nike Football Replica 3-Piece Kit | £54.99
Nike Tiempo Maestro Elite LE Firm-Ground Low-Top Football Boot | £239.99
Bestseller | Nike Academy Older Kids' Dri-FIT Long-Sleeve 1/4-Zip Football Drill Top | £32.99
Coming Soon | Nike Mind 002 Men's Shoes | £129.99
Recycled Materials | Nike Tiempo Maestro Club Multi-Ground Low-Top Football Boots | £54.99
Air Jordan Ultra Men's Shoes | £129.99
Recycled Materials | Nike Kids' Backpack (20L) | £29.99
Bestseller | FC Barcelona 2026 Stadium Home Younger Kids' Nike Football Replica 3-Piece Kit | £54.99
Nike United Phantom 6 Low Academy Turf Football Shoes | £84.99
Nike Tiempo Ligera Pro LE Firm-Ground Low-Top Football Boot | £144.99
Recycled Materials | Paris Saint-Germain 2026 Match Night Edition Men's Jordan Dri-FIT ADV Football Authentic Shirt | £124.99
Recycled Materials | Nike Swoosh Women's Medium-Support Padded Sports Bra | £39.99
Nike Air Force 1 '07 LVB 'USA' Men's Shoes | £109.99
Recycled Materials | Nike Academy Men's Dri-FIT Football Shorts | £22.99
Recycled Materials | Nike Academy Men's Dri-FIT Football Pants | £39.99
Recycled Materials | Brazil 2026 Match Away Men's Jordan Aero-FIT Football Authentic Shirt | £134.99
Recycled Materials | Nike Academy Older Kids' Dri-FIT Football Top | £16.99
Nike Js Mercurial Vapor 16 Academy 'Vini Jr.' Older Kids' Multi-Ground Low-Top Football Boot | £64.99
Nike Js Phantom 6 Low Pro 'Erling Haaland' Older Kids' Multi-ground Football Boot | £109.99
Nike Air Max Plus 'Flairemax' Men's Shoes | £184.99
Recycled Materials | England 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shorts | £34.99
Recycled Materials | Nike Js Phantom 6 Low Academy 'Erling Haaland' Older Kids' Artificial-grass Football Boot | £59.99
Recycled Materials | Nike Academy Older Kids' Dri-FIT Football Shorts | £14.99
England Primary Men's Nike Dri-FIT Football T-Shirt | £49.99
Nike United Js Mercurial Vapor 16 Academy Older Kids' Multi-Ground Low-Top Football Boot | £64.99
Nike Jr Phantom 6 Low Academy 'Alexia Putellas' Older Kids' Multi-Ground Football Boot | £64.99
Coming Soon | Nike Mind 002 Men's Shoes | £129.99
Recycled Materials | England Strike Men's Nike Football Dri-FIT Short-Sleeve Top | £49.99
Recycled Materials | Paris Saint-Germain 2025/26 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £84.99
Nike Js Phantom 6 Low Club Older Kids' Multi-ground Football Boot | £44.99
Nike United Phantom 6 Low Academy Multi-ground Football Boot | £84.99
Nike Air Max Plus OG 'FFF' Men's Shoes | £174.99
Recycled Materials | England 2026 Stadium Home Younger Kids' Nike Football Replica 3-Piece Kit | £54.99
Nike United Jr Phantom 6 Low Academy Older Kids' Multi-Ground Football Boot | £59.99
Recycled Materials | Paris Saint-Germain 2026 Stadium Night Edition Men's Jordan Dri-FIT Football Replica Shirt | £84.99
Nike United Tiempo Maestro Academy Turf Low-Top Football Shoes | £79.99
Jordan Essentials Men's Boxy T-Shirt | £39.99
Recycled Materials | Nike Tiempo Maestro Club Turf Low-Top Football Shoes | £54.99
Nike United Mercurial Vapor 16 Academy Multi-Ground Low-Top Football Boots | £84.99
Nike Js Phantom 6 Low Academy 'Erling Haaland' Older Kids' Multi-ground Football Boot | £59.99
Nike United Js Mercurial Superfly 10 Academy Older Kids' Multi-Ground High-Top Football Boot | £69.99
Nike United Phantom 6 High Academy Multi-ground Football Boot | £89.99
Recycled Materials | F.C. Barcelona 2025/26 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £84.99
Bestseller | Nike United Phantom 6 High Elite Firm-Ground Football Boot | £264.99
Coming Soon | Nike Mind 002 Men's Shoes | £129.99
Nike Js Phantom 6 Low Academy 'Erling Haaland' Older Kids' Turf Football Shoe | £59.99
Bestseller | Paris Saint-Germain 2025/26 Stadium Fourth Men's Jordan Dri-FIT Football Replica Shirt | £84.99
Stade Toulousain X Toulouse F.C. Unisex Nike Capitolium Pique Polo | £34.99
Coming Soon | Nike Mind 001 Men's Pregame Mules | £79.99
Coming Soon | Nike Mind 001 Women's Pregame Mules | £79.99
Nike Phantom 6 Low Elite LV8 Firm-Ground Football Boot | £254.99
Recycled Materials | Nike Js Tiempo Maestro Club MG Low-Top Football Boot | £39.99
Nike United Mercurial Superfly 10 Academy Multi-Ground High-Top Football Boot | £89.99
Recycled Materials | England 2026 Stadium Goalkeeper Older Kids' Nike Dri-FIT Football Replica Short-Sleeve Shirt | £69.99
Recycled Materials | England 2026 Stadium Goalkeeper Women's Nike Dri-FIT Football Replica Short-Sleeve Shirt | £89.99
Bestseller | Nike Phantom 6 Low Elite Firm-Ground Football Boot | £171.49
Recycled Materials | Nike Phantom 6 High Elite Firm-Ground Football Boot | £178.49
Bestseller | Nike Mercurial Vapor 16 Elite Firm-Ground Low-Top Football Boot | £171.49
Recycled Materials | Nike Mercurial Superfly 10 Elite Firm-Ground High-Top Football Boot | £178.49
Recycled Materials | England 2026 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | England 2026 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £69.99
Recycled Materials | England 2026 Stadium Home Women's Nike Dri-FIT Football Replica Shirt | £89.99
Nike Air Max 95 Big Bubble 'England' Men's Shoes | £174.99
Coming Soon | England Men's Nike Dri-FIT Football Anthem Jacket | £109.99
Recycled Materials | England 2026 Stadium Goalkeeper Men's Nike Dri-FIT Football Replica Short-Sleeve Shirt | £89.99
Recycled Materials | Brazil 2026 Stadium Away Older Kids' Jordan Dri-FIT Football Replica Shirt | £69.99
Just In | Nike Strike Older Kids' Dri-FIT Football Short-Sleeve Top | £27.99
Just In | Nike Strike Older Kids' Dri-FIT Football Shorts | £27.99
Just In | Nike Strike Men's Dri-FIT Short-Sleeve Football Shirt | £39.99
Just In | Nike Strike Men's Dri-FIT Football Shorts | £37.99
Just In | Nike Strike Men's Dri-FIT Football Drill Top | £59.99
Recycled Materials | Uruguay 2026 Stadium Away Men's Nike Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | FFF 2026 Match Home Older Kids' Nike Aero-FIT Football Authentic Jersey | £114.99
Recycled Materials | Norway 2026 Stadium Away Older Kids' Nike Dri-FIT Football Replica Shirt | £69.99
Recycled Materials | Brazil 2026 Match Home Older Kids' Nike Aero-FIT Football Authentic Jersey | £114.99
Recycled Materials | Brazil 2026 Stadium Away Older Kids' Jordan Dri-FIT Football Replica Shirt | £69.99
Just In | Nike Strike Older Kids' Dri-FIT Football Short-Sleeve Top | £27.99
Coming Soon | Norway 2026 Match Away Men's Nike Aero-FIT Football Authentic Jersey | £134.99
Coming Soon | Brazil 2026 Match Home Men's Nike Aero-FIT Football Authentic Jersey | £134.99
Recycled Materials | Brazil 2026 Stadium Away Men's Jordan Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | Norway 2026 Match Home Older Kids' Nike Aero-FIT Football Authentic Jersey | £114.99
Recycled Materials | Norway 2026 Stadium Away Men's Nike Dri-FIT Football Replica Shirt | £89.99
Recycled Materials | Norway 2026 Stadium Away Women's Nike Dri-FIT Football Replica Shirt | £89.99
Coming Soon | England 2026 Match Home Men's Nike Aero-FIT Football Authentic Jersey | £134.99
Sold Out | England 2026 Match Away Older Kids' Nike Aero-FIT Football Authentic Jersey | £114.99
Recycled Materials | FFF 2026 Match Home Men's Nike Aero-FIT Football Authentic Shirt | £134.99
Just In | FFF 2026 Match Home Women's Nike Aero-FIT Football Authentic Jersey | £134.99
Recycled Materials | Netherlands 2026 Match Home Men's Nike Aero-FIT Football Authentic Shirt | £134.99
Recycled Materials | Netherlands 2026 Match Home Older Kids' Nike Aero-FIT Football Authentic Jersey | £114.99
Just In | Paris Saint-Germain 2026/27 Stadium Goalkeeper Women's Nike Dri-FIT Football Replica Shirt | £99.99
Just In | Paris Saint-Germain 2026/27 Stadium Goalkeeper Older Kids' Nike Dri-FIT Football Replica Shirt | £74.99
Nike United Jr. Mercurial Vapor 16 Pro Older Kids' Firm-Ground Low-Top Football Boot | £129.99
Nike United Women's Football T-Shirt | £37.99
Recycled Materials | Nike United Academy Women's Dri-FIT Football Knit Shorts | £22.99
Nike United Jr Phantom 6 Low Pro Older Kids' Multi-Ground Football Boot | £109.99
Nike United Tiempo Maestro Elite Firm-Ground Low-Top Football Boot | £239.99
Nike Tiempo Ligera Pro Firm-Ground Low-Top Football Boot | £134.99
Just In | Paris Saint-Germain 2026/27 Stadium Home Men's Nike Dri-FIT Football Replica Shirt | £89.99
Just In | Paris Saint-Germain 2026/27 Stadium Home Older Kids' Nike Dri-FIT Football Replica Shirt | £69.99
Coming Soon | Paris Saint-Germain 2026/27 Match Home Men's Nike Aero-FIT Football Authentic Shirt | £134.99
Just In | Paris Saint-Germain 2026/27 Stadium Home Men's Nike Dri-FIT Football Replica Long-Sleeve Shirt | £99.99
Coming Soon | Jordan Tiempo Maestro Elite SE Firm-Ground Low-Top Football Boot | £244.99
Just In | Nike Mercurial Superfly 10 Elite LV8 Firm-Ground High-Top Football Boot | £264.99
Just In | Nike Mercurial Vapor 16 Elite LV8 Firm-Ground Low-Top Football Boot | £254.99
Nike Tiempo Maestro Elite Firm-Ground Low-Top Football Boot | £229.99
Bestseller | Nike United Phantom 6 Low Elite Firm-Ground Football Boot | £254.99
Nike United Mercurial Vapor 16 Elite Firm-Ground Low-Top Football Boot | £254.99
Just In | Nike Phantom 6 Low Elite LV8 Firm-Ground Football Boot | £254.99
Just In | Nike Phantom 6 High Elite LV8 Firm-Ground Football Boot | £264.99
Just In | Nike Tiempo Maestro Elite LV8 Firm-Ground Low-Top Football Boot | £239.99
Nike Phantom 6 Low Elite 'Erling Haaland' Firm-Ground Football Boot | £254.99
Nike Phantom 6 Low Elite 'Erling Haaland' Artificial-Grass Football Boot | £254.99
Jordan Tiempo Streetgato SE Indoor Court Low-Top Football Shoes | £89.99
"""

# ─── Parse products ───────────────────────────────────────────────────────────
def parse_products(raw_text):
    products = []
    seen = set()
    TAGS = {"Recycled Materials", "Bestseller", "Sold Out", "Just In", "Coming Soon"}
    for line in raw_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Split on last " | "
        parts = [p.strip() for p in line.split(" | ")]
        if len(parts) >= 2:
            price_str = parts[-1]
            if price_str.startswith("£"):
                name_parts = parts[:-1]
                tag = None
                if name_parts[0] in TAGS:
                    tag = name_parts[0]
                    name = " | ".join(name_parts[1:])
                else:
                    name = " | ".join(name_parts)
                try:
                    price = float(price_str.replace("£", "").replace(",", ""))
                except:
                    continue
                key = (name.lower(), price)
                if key not in seen:
                    seen.add(key)
                    products.append({"name": name, "price": price, "price_str": price_str, "tag": tag})
    return products

products = parse_products(raw)

# ─── Categorise ───────────────────────────────────────────────────────────────
def categorise(p):
    n = p["name"].lower()
    if any(x in n for x in ["boot", "shoe", "turf", "firm-ground", "soft-ground",
                             "multi-ground", "artificial-grass", "indoor court",
                             "tiempo", "phantom", "mercurial", "premier 3",
                             "reactgato", "streetgato"]):
        return "Footwear"
    if any(x in n for x in ["shirt", "jersey", "top", "t-shirt", "polo", "kit",
                             "replica", "authentic", "goalkeeper shirt"]):
        return "Shirts & Kits"
    if any(x in n for x in ["short", "pant", "trouser", "jogger", "track",
                             "knit pant", "knit short", "woven"]):
        return "Bottoms & Trousers"
    if any(x in n for x in ["jacket", "hoodie", "fleece", "windrunner", "sweatshirt",
                             "pullover", "anthem", "shell", "zip"]):
        return "Jackets & Hoodies"
    if any(x in n for x in ["bag", "backpack", "gymsack", "duffel"]):
        return "Bags & Accessories"
    if any(x in n for x in ["ball", "shinguard", "glove", "sock", "sleeve",
                             "snood", "cap", "hat", "slide", "mule", "bra"]):
        return "Accessories & Equipment"
    return "Apparel"

categories = {}
for p in products:
    cat = categorise(p)
    categories.setdefault(cat, []).append(p)

CAT_ORDER = [
    "Footwear", "Shirts & Kits", "Jackets & Hoodies",
    "Bottoms & Trousers", "Bags & Accessories", "Accessories & Equipment", "Apparel"
]

# ─── Colors ───────────────────────────────────────────────────────────────────
NIKE_BLACK  = colors.HexColor("#111111")
NIKE_RED    = colors.HexColor("#FA4616")   # Nike orange-red
ACCENT_GREY = colors.HexColor("#F5F5F5")
MID_GREY    = colors.HexColor("#E0E0E0")
DIM_GREY    = colors.HexColor("#888888")
WHITE       = colors.white

TAG_COLORS = {
    "Bestseller":       (colors.HexColor("#FFD700"), NIKE_BLACK),
    "Just In":          (colors.HexColor("#4CAF50"), WHITE),
    "Coming Soon":      (colors.HexColor("#2196F3"), WHITE),
    "Sold Out":         (colors.HexColor("#9E9E9E"), WHITE),
    "Recycled Materials": None,  # shown as small green dot
}

W, H = A4

# ─── Document ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "nike_football_catalog.pdf",
    pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=20*mm, bottomMargin=20*mm,
)

styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

# Style definitions
s_cover_title = S("CoverTitle",
    fontName="Helvetica-Bold", fontSize=52, textColor=WHITE,
    leading=60, alignment=TA_LEFT, spaceAfter=6)

s_cover_sub = S("CoverSub",
    fontName="Helvetica", fontSize=16, textColor=colors.HexColor("#CCCCCC"),
    leading=22, alignment=TA_LEFT)

s_section = S("Section",
    fontName="Helvetica-Bold", fontSize=20, textColor=WHITE,
    leading=26, alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)

s_item_name = S("ItemName",
    fontName="Helvetica", fontSize=7.5, textColor=NIKE_BLACK,
    leading=11, alignment=TA_LEFT)

s_item_price = S("ItemPrice",
    fontName="Helvetica-Bold", fontSize=9, textColor=NIKE_BLACK,
    leading=12, alignment=TA_LEFT)

s_tag = S("Tag",
    fontName="Helvetica-Bold", fontSize=6, textColor=WHITE,
    leading=8, alignment=TA_LEFT)

s_footer = S("Footer",
    fontName="Helvetica", fontSize=7, textColor=DIM_GREY,
    leading=10, alignment=TA_CENTER)

s_toc_cat = S("TocCat",
    fontName="Helvetica-Bold", fontSize=11, textColor=NIKE_BLACK,
    leading=16, alignment=TA_LEFT)

s_toc_count = S("TocCount",
    fontName="Helvetica", fontSize=10, textColor=DIM_GREY,
    leading=14, alignment=TA_RIGHT)

story = []

# ─── Page 1: Cover ────────────────────────────────────────────────────────────
from reportlab.platypus import Flowable

class BlackRect(Flowable):
    def __init__(self, w, h, fill_color=NIKE_BLACK):
        super().__init__()
        self.w, self.h, self.fill_color = w, h, fill_color
        self._width, self._height = w, h
    def draw(self):
        self.canv.setFillColor(self.fill_color)
        self.canv.rect(0, 0, self.w, self.h, fill=1, stroke=0)

class FullPageCover(Flowable):
    """Full A4 cover drawn on canvas."""
    def __init__(self, total_products):
        super().__init__()
        self.total = total_products
    def wrap(self, aw, ah):
        return (aw, ah)
    def draw(self):
        c = self.canv
        # Background
        c.setFillColor(NIKE_BLACK)
        c.rect(-18*mm, -H+20*mm, W, H, fill=1, stroke=0)  # cover whole area

        # Red accent bar
        c.setFillColor(NIKE_RED)
        c.rect(-18*mm, H/2 - 20*mm, 8*mm, 80*mm, fill=1, stroke=0)

        # NIKE wordmark area (bold big text)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 72)
        c.drawString(0, H - 80*mm, "NIKE")

        c.setFont("Helvetica-Bold", 36)
        c.setFillColor(NIKE_RED)
        c.drawString(0, H - 110*mm, "FOOTBALL")

        # Subtitle
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.HexColor("#AAAAAA"))
        c.drawString(0, H - 128*mm, "Product Catalogue  ·  2025/26 Season")

        # Divider
        c.setStrokeColor(NIKE_RED)
        c.setLineWidth(1.5)
        c.line(0, H - 138*mm, W - 36*mm, H - 138*mm)

        # Stats row
        c.setFont("Helvetica-Bold", 28)
        c.setFillColor(WHITE)
        c.drawString(0, H - 162*mm, str(self.total))
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#AAAAAA"))
        c.drawString(0, H - 174*mm, "products listed")

        cats_count = sum(1 for c2 in CAT_ORDER if c2 in categories)
        c.setFont("Helvetica-Bold", 28)
        c.setFillColor(WHITE)
        c.drawString(80*mm, H - 162*mm, str(cats_count))
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#AAAAAA"))
        c.drawString(80*mm, H - 174*mm, "categories")

        # Footer
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0, 20*mm, "nike.com/gb  ·  All prices in GBP  ·  As of May 2026")

from reportlab.platypus import PageBreak

story.append(FullPageCover(len(products)))
story.append(PageBreak())

# ─── Page 2: Contents ─────────────────────────────────────────────────────────

story.append(PageBreak())

# Header bar for contents
class SectionHeader(Flowable):
    def __init__(self, text, width):
        super().__init__()
        self._width = width
        self._height = 14*mm
        self.text = text
    def wrap(self, aw, ah):
        return (self._width, self._height)
    def draw(self):
        c = self.canv
        c.setFillColor(NIKE_BLACK)
        c.rect(0, 0, self._width, self._height, fill=1, stroke=0)
        c.setFillColor(NIKE_RED)
        c.rect(0, 0, 4*mm, self._height, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(8*mm, 4*mm, self.text)

usable_w = W - 36*mm

story.append(SectionHeader("CONTENTS", usable_w))
story.append(Spacer(1, 6*mm))

toc_data = []
for cat in CAT_ORDER:
    if cat not in categories:
        continue
    cnt = len(categories[cat])
    toc_data.append([
        Paragraph(cat, s_toc_cat),
        Paragraph(f"{cnt} items", s_toc_count),
    ])

toc_table = Table(toc_data, colWidths=[usable_w*0.75, usable_w*0.25])
toc_table.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, ACCENT_GREY]),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LINEBELOW", (0,0), (-1,-1), 0.5, MID_GREY),
]))
story.append(toc_table)
story.append(Spacer(1, 8*mm))

total_price = sum(p["price"] for p in products)
avg_price = total_price / len(products) if products else 0
prices_sorted = sorted(p["price"] for p in products)
min_p = prices_sorted[0]
max_p = prices_sorted[-1]

summary_data = [
    ["Total Products", f"{len(products)}"],
    ["Avg. Price", f"£{avg_price:.2f}"],
    ["Price Range", f"£{min_p:.2f} – £{max_p:.2f}"],
]
sum_table = Table(summary_data, colWidths=[usable_w*0.5, usable_w*0.5])
sum_table.setStyle(TableStyle([
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTNAME", (1,0), (1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("TEXTCOLOR", (0,0), (0,-1), NIKE_BLACK),
    ("TEXTCOLOR", (1,0), (1,-1), colors.HexColor("#444444")),
    ("BACKGROUND", (0,0), (-1,0), ACCENT_GREY),
    ("BACKGROUND", (0,1), (-1,1), WHITE),
    ("BACKGROUND", (0,2), (-1,2), ACCENT_GREY),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("BOX", (0,0), (-1,-1), 0.5, MID_GREY),
    ("INNERGRID", (0,0), (-1,-1), 0.5, MID_GREY),
]))
story.append(sum_table)

# ─── Category pages ───────────────────────────────────────────────────────────
COLS = 3
CELL_W = usable_w / COLS
CELL_H = 28*mm  # fixed row height

for cat in CAT_ORDER:
    if cat not in categories:
        continue
    prods = sorted(categories[cat], key=lambda x: x["name"])

    story.append(PageBreak())
    story.append(SectionHeader(cat.upper(), usable_w))
    story.append(Spacer(1, 4*mm))

    # Build grid rows of COLS cells
    rows = []
    row = []
    for i, p in enumerate(prods):
        name = p["name"]
        price_str = p["price_str"]
        tag = p["tag"]

        # Tag badge text
        tag_cell = ""
        eco = ""
        if tag == "Recycled Materials":
            eco = '<font color="#2E7D32">●</font> '
        elif tag in ("Bestseller", "Just In", "Coming Soon", "Sold Out"):
            tc = {"Bestseller": "#D4A017", "Just In": "#2E7D32",
                  "Coming Soon": "#1565C0", "Sold Out": "#757575"}[tag]
            tag_cell = f'<font color="{tc}"><b>[{tag.upper()}]</b></font>  '

        cell_content = [
            Paragraph(f'{eco}<b>{tag_cell}</b>{name}', s_item_name),
            Spacer(1, 2),
            Paragraph(price_str, s_item_price),
        ]
        row.append(cell_content)
        if len(row) == COLS:
            rows.append(row)
            row = []
    if row:
        while len(row) < COLS:
            row.append([Paragraph("", s_item_name)])
        rows.append(row)

    # Flatten into Table
    flat_rows = []
    for row in rows:
        flat_rows.append([
            Table([[cell_content[0]], [cell_content[1]], [cell_content[2]]],
                  colWidths=[CELL_W - 6*mm])
            if len(cell_content) == 3 else
            Table([[cell_content[0]]], colWidths=[CELL_W - 6*mm])
            for cell_content in row
        ])

    grid = Table(flat_rows, colWidths=[CELL_W]*COLS, rowHeights=[CELL_H]*len(flat_rows))
    grid.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, ACCENT_GREY]),
        ("LINEBELOW", (0,0), (-1,-1), 0.3, MID_GREY),
        ("LINEBEFORE", (1,0), (1,-1), 0.3, MID_GREY),
        ("LINEBEFORE", (2,0), (2,-1), 0.3, MID_GREY),
        ("BOX", (0,0), (-1,-1), 0.5, MID_GREY),
    ]))
    story.append(grid)

# ─── Back page ────────────────────────────────────────────────────────────────
story.append(PageBreak())
class BackCover(Flowable):
    def wrap(self, aw, ah):
        return (aw, ah)
    def draw(self):
        c = self.canv
        c.setFillColor(NIKE_BLACK)
        c.rect(-18*mm, -H+20*mm, W, H, fill=1, stroke=0)
        c.setFillColor(NIKE_RED)
        c.setFont("Helvetica-Bold", 96)
        c.drawCentredString(W/2 - 18*mm, H/2 - 10*mm, "✓")
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(WHITE)
        c.drawCentredString(W/2 - 18*mm, H/2 - 36*mm, "Just Do It.")
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor("#666666"))
        c.drawCentredString(W/2 - 18*mm, 15*mm, "nike.com/gb  ·  football")

story.append(BackCover())

# ─── Build ────────────────────────────────────────────────────────────────────
doc.build(story)
print("Done! Products:", len(products))