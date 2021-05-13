package org.opwo.gradle

class FileData {
    String name
    long size
    String url
    HashObject hash

    FileData(String name, long size, String url, HashObject hash) {
        this.name = name
        this.size = size
        this.url = url
        this.hash = hash
    }
}
