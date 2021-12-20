from pprint import pprint
import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://postgres:py45@localhost:5432/hw_4')

connection = engine.connect()

# 1. количество исполнителей в каждом жанре;
sel = connection.execute('''
# SELECT genre_name gn, COUNT(artist_id) art_id FROM genres g
# JOIN list1 l1 ON g.genre_id = l1.genre_id
# GROUP BY gn
# ORDER BY art_id DESC;
# ''').fetchall()
print(sel)

# 2. количество треков, вошедших в альбомы 2019-2020 годов;
sel = connection.execute('''
SELECT year y, COUNT(track_id) tr_id  FROM albums a
JOIN  tracks t ON a.album_id = t.album_id
WHERE (year >=2019) AND (year <= 2020)
GROUP BY y;
''').fetchall()
print(sel)

# 3.средняя продолжительность треков по каждому альбому;
sel = connection.execute('''
SELECT album_name an, AVG(time) FROM albums a
JOIN  tracks t ON a.album_id = t.album_id
GROUP BY an;
''').fetchall()
pprint(sel)

# 4.все исполнители, которые не выпустили альбомы в 2020 году;
sel = connection.execute('''
SELECT DISTINCT name n FROM artists a
JOIN list2 l2 ON a.artist_id = l2.artist_id
JOIN albums al ON al.album_id = l2.album_id
WHERE NOT al.year = '2020'
ORDER BY n;
''').fetchall()
pprint(sel)

# 5.названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
sel = connection.execute('''
SElECT  DISTINCT collection_name FROM  collection c
JOIN list3 l3  ON c.collection_id = l3.collection_id
JOIN tracks t ON l3.track_id = t.track_id
JOIN albums al ON t.album_id = al.album_id
JOIN list2 l2 ON al.album_id = l2.album_id
JOIN artists a ON l2.artist_id = a.artist_id
WHERE a.artist_id = 6;
''').fetchall()
print(sel)

# 6.название альбомов, в которых присутствуют исполнители более 1 жанра;
sel = connection.execute('''
SELECT album_name an FROM albums al
JOIN list2 l2 ON al.album_id = l2.album_id
JOIN artists a ON l2.artist_id = a.artist_id
JOIN list1 l1 ON a.artist_id = l1.artist_id
JOIN genres g ON l1.genre_id = g.genre_id
GROUP BY an
HAVING COUNT(genre_name) > 1;
''').fetchall()
print(sel)

# 7.наименование треков, которые не входят в сборники;
sel = connection.execute('''
SELECT title FROM tracks
WHERE track_id NOT IN(SELECT track_id FROM  list3)
''').fetchall()
print(sel)

# 8.исполнителя(-ей), написавшего самый короткий по продолжительности трек
# (теоретически таких треков может быть несколько);
sel = connection.execute('''
SELECT a.name, t.time FROM tracks t
JOIN albums al  ON al.album_id = t.album_id
JOIN list2 l2 ON l2.album_id = al.album_id
JOIN artists a ON a.artist_id = l2.artist_id
GROUP BY a.name, t.time
HAVING t.time = (SELECT MIN(time) FROM tracks)
ORDER BY a.name;
''').fetchall()
pprint(sel)


# 9.название альбомов, содержащих наименьшее количество треков.
sel = connection.execute('''
SELECT album_name FROM albums a
LEFT JOIN tracks t ON t.album_id = a.album_id
WHERE t.album_id IN (
SELECT album_id FROM tracks
GROUP BY album_id
HAVING COUNT (album_id) = (
SELECT COUNT (album_id) FROM tracks
GROUP BY album_id
ORDER BY COUNT
LIMIT 1))
ORDER BY album_name
''').fetchall()
print(sel)
