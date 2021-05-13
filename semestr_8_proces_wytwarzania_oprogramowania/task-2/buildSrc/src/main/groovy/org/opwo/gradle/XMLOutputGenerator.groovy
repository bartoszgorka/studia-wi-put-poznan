package org.opwo.gradle

import groovy.xml.MarkupBuilder

import java.text.SimpleDateFormat

class XMLOutputGenerator {
    File outputFile
    MetalinkCollection collection

    XMLOutputGenerator(File outputFile, MetalinkCollection collection) {
        this.outputFile = outputFile
        this.collection = collection
    }

    void generateXML() {
        // Output file and content builder
        FileWriter fileWriter = new FileWriter(outputFile)
        MarkupBuilder builder = new MarkupBuilder(fileWriter)
        builder.setDoubleQuotes(true)

        // Add header
        builder.mkp.xmlDeclaration(version: "1.0", encoding: "utf-8")

        // Add content
        builder.metalink(xmls: "urn:ietf:params:xml:ns:metalink") {
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'")
            dateFormat.setTimeZone(TimeZone.getTimeZone("GMT"))
            published(dateFormat.format(collection.published_at))
            collection.files.each { f ->
                file(name: f.name) {
                    size(f.size)
                    hash(type: f.hash.type, f.hash.value)
                    url(f.url)
                }
            }
        }

        // Save file
        fileWriter.close()
    }
}
