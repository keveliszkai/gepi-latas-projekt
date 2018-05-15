# gepi-latas-projekt

## Dependencies

opencv 3, darknet, python.

## Scripts

A mappa struktúrát létrehozó script

```
init.sh
```

A Raspberry-n futó main, verziószámmal

```
python main_rasp_${version}.py
```

A Raspberry-n futó main-t elindító scriptek

```
python start_${version}.sh
```

A harmadik és második verzióhoz tartozó utó feldolgozó script.

```
python post-process.py
```

A képeket archiváló script

```
archive.sh
```

A kép beállítását segítő scriptek.

```
python view.py
python view_rasp.py
```

## Mappák

A kategorizált képeket tartalmazó mappák.

```
cat/
dog/
person/
others/
```

Az érdemben működő OpenCV próbálkozások.

```
OpenCV/
```

A post-process által feldolgozni kívánt képek.

```
input/
```
