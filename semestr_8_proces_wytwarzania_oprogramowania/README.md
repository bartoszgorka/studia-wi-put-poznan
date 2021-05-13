# Code development process
Study project - Poznan University of Technology

Intelligent Information Technologies @ 2019

## Task 1
Napisz zadanie list symulujące działanie polecenia systemowego listującego pliki i katalogi wskazanego katalogu, konfigurowalne za pomocą własności `fileSet`. Zadanie to powinno być zaimplementowane w klasie `DirList`,  zdefiniowanej wewnątrz pliku `build.gradle`.

## Task 2
Napisz własne zadanie metalink typu `Metalink` wspomagające dystrybucję oprogramowania, konfigurowalne za pomocą własności `fileSet`, `url` oraz `outputFile`. Akcje tego zadania mają być opisane w zewnętrznej klasie `Metalink` (pakiet `org.opwo.gradle`), napisanej w języku Groovy (ew. Java).

Zadanie ma umożliwiać generowanie pliku w formacie `Metalink 4.0`, zawierającego m.in. adresy URL dystrybuowanych plików (adresy pod którymi docelowo będą dystrybuowane) oraz hash md5 tych plików do sprawdzenia poprawności dystrybucji, jak również inne sensowne elementy standardu Metalink (co najmniej takie jak w przykładzie poniżej).

Bazowy adres URL, pod którym będą dystrybuowane pliki, jak również ścieżka do generowanego pliku Metalink mają być własnościami zadania (własności `url` oraz `outputFile`). Dodatkowo jeśli bazowy URL nie jest podany, domyślny URL ma być odczytany z własności Gradle’a o nazwie `serverFilesUrl` (z pliku `gradle.properties`).

Należy uwzględnić wszystkie pliki znajdujące się bezpośrednio w katalogu wskazywanym przez właściwość `fileSet`, a także w jego podkatalogach (rekurencyjnie). W wygenerowanym wynikowym pliku xml, znacznik url pliku powinien uwzględniać podkatalogi, względem katalogu głównego dystrybucji wskazywanego przez własność `fileSet`.

Kod klasy powinien znajdować się w katalogu `buildSrc/src/main/groovy/org/opwo/gradle` (ew. w katalogu `buildSrc/src/main/java/org/opwo/gradle`); katalog `buildSrc` powinien znajdować się w głównym katalogu dystrybuowanego oprogramowania, podobnie jak skrypt `build.gradle`.
