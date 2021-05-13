package search;

import engine.Document;

import java.util.ArrayList;
import java.util.Collections;

public class CosineSimilarity_TF_IDF implements ISearch {
    private ArrayList<Document> _documents;

    public CosineSimilarity_TF_IDF(ArrayList<Document> documents) {
        this._documents = documents;
    }

    @Override
    public ArrayList<Score> getSortedDocuments(Document query) {
        return getSortedDocuments(query._tf_idf_representation);
    }

    @Override
    public ArrayList<Score> getSortedDocuments(double[] queryVector) {
        ArrayList<Score> scores = new ArrayList<>(_documents.size());
        // update scores: compute a similarity of each document (TF-IDF) to the query vector
        // -----------------------------------------------
        double sum_query = 0.0;
        for (double value : queryVector) {
            sum_query += Math.pow(value, 2);
        }

        for (Document document : _documents) {
            double counter = 0.0;
            double sum_document = 0.0;
            for (int i = 0; i < queryVector.length; i++) {
                double document_value = document._tf_idf_representation[i];
                counter += (queryVector[i] * document_value);
                sum_document += Math.pow(document_value, 2);
            }
            scores.add(new Score(document, counter / Math.sqrt(sum_document * sum_query)));
        }

        // -----------------------------------------------

        Collections.sort(scores);
        return scores;
    }

    @Override
    public String getName() {
        return "Cosine similarity";
    }
}
