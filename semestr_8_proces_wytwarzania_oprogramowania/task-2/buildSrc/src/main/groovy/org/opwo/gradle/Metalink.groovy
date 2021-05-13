package org.opwo.gradle

import groovy.io.FileType
import org.gradle.api.DefaultTask
import org.gradle.api.tasks.TaskAction

import java.security.DigestInputStream
import java.security.MessageDigest

class Metalink extends DefaultTask {
    String fileSet
    String url
    String outputFile
    MetalinkCollection collection = new MetalinkCollection()

    @TaskAction
    void build() {
        // Set URL from properties when user ignored it in build.gradle
        if (this.url == null) {
            this.url = project.properties["serverFilesUrl"]
        }

        // For each file prepare MD5 hash
        generateMD5()

        // Generate XML
        File output = generateOutputFile()
        XMLOutputGenerator generator = new XMLOutputGenerator(output, collection)
        generator.generateXML()
    }

    File generateOutputFile() {
        File output = new File(outputFile)
        output.createNewFile()

        return output
    }

    void generateMD5() {
        File dir = new File(fileSet)
        dir.eachFileRecurse(FileType.FILES) { file ->
            if (file.isFile()) {
                String filePath = file.getAbsolutePath().toString() - dir.getAbsolutePath().toString()
                URL urlObj = new URL(url + filePath)
                FileData fileData = new FileData(file.name, file.length(), urlObj.toString(), calculateMD5Hash(file))
                collection.addFile(fileData)
            }
        }
    }

    static HashObject calculateMD5Hash(File file) {
        String hash = file.withInputStream {
            new DigestInputStream(it, MessageDigest.getInstance('MD5')).withStream {
                it.eachByte {}
                it.messageDigest.digest().encodeHex() as String
            }
        }

        return new HashObject("MD5", hash)
    }
}
