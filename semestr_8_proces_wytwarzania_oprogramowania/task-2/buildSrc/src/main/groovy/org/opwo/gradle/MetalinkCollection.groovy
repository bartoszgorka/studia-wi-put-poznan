package org.opwo.gradle

class MetalinkCollection {
    List<FileData> files
    Date published_at

    MetalinkCollection() {
        this.files = new ArrayList<>()
        this.published_at = new Date()
    }

    void addFile(FileData file) {
        this.files.add(file)
    }
}
