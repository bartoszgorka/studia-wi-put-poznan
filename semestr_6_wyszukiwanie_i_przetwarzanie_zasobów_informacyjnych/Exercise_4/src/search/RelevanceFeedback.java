package search;

import engine.Document;

import java.util.ArrayList;

public class RelevanceFeedback implements ISearch {
    private ArrayList<Document> _documents;
    private double _alpha;
    private double _beta;
    private double _gamma;
    private int _relevantDocIDs[];
    private int _irrelevantDocIDs[];

    public RelevanceFeedback(ArrayList<Document> documents,
                             double alpha,
                             double beta,
                             double gamma,
                             int _relevantDocIDs[],
                             int _irrelevantDocIDs[]) {
        this._documents = documents;
        this._alpha = alpha;
        this._beta = beta;
        this._gamma = gamma;
        this._relevantDocIDs = _relevantDocIDs;
        this._irrelevantDocIDs = _irrelevantDocIDs;
    }

    @Override
    public ArrayList<Score> getSortedDocuments(Document query) {
        return getSortedDocuments(query._tf_idf_representation);
    }

    @Override
    public ArrayList<Score> getSortedDocuments(double[] queryVector) {
        System.out.println("TF-IDF representation = ");
        for (double aQueryVector : queryVector)
            System.out.print(String.format("%.2f ", aQueryVector));
        System.out.println("");

        // DONE implement Rocchio method for relevance feedback
        // use _tf_idf_representation of documents,
        // alpha, betta, and gamma are the weights,
        // relevantDocIDs is the vector of IDs of relevant documents (id = index),
        // irrelevantDocIDs is the vector of IDs of irrelevant documents (id = index)
        //-----------------------------------------------------------
        double modifiedQuery[] = new double[queryVector.length];
        // -----------------------------------------------
        // use _alpha
        // -----------------------------------------------

        // DONE 2) update the modified query (relevant documents).
        // 1) iterate over the indexes of the relevant documents
        // 2) derive the vector representation (tf-idf) of a document
        // 3) update the modifiedQuery vector (add, beta weight, divide by the number of relevant documents)

        // -----------------------------------------------
        // -----------------------------------------------


        // DONE 3)  update the modified query
        // 1) iterate over the indexes of the irrelevant documents
        // 2) derive the vector representation (tf-idf) of a document
        // 3) update the modifiedQuery vector (substract, gamma weight, divide by the number of irrelevant documents)

        // -----------------------------------------------
        // -----------------------------------------------
        double relevantDocumentsSize = (double) _relevantDocIDs.length;
        double irRelevantDocumentsSize = (double) _irrelevantDocIDs.length;

        for (int i = 0; i < queryVector.length; i++) {
            double relevant = 0.0d;
            double irRelevant = 0.0d;

            // Relevant documents
            for (int relevantDocID : _relevantDocIDs) {
                relevant += _documents.get(relevantDocID)._tf_idf_representation[i];
            }

            // IrRelevant documents
            for (int irrelevantDocID : _irrelevantDocIDs) {
                irRelevant += _documents.get(irrelevantDocID)._tf_idf_representation[i];
            }

            // Calculate results
            modifiedQuery[i] = _alpha * queryVector[i]
                    + _beta * (1 / relevantDocumentsSize) * relevant
                    - _gamma * (1 / irRelevantDocumentsSize) * irRelevant;
        }


        // -----------------------------------------------

        System.out.println("Modified TF-IDF representation = ");
        for (double aQueryVector : modifiedQuery)
            System.out.print(String.format("%.2f ", aQueryVector));
        System.out.println("");

        ISearch search = new CosineSimilarity_TF_IDF(_documents);
        return search.getSortedDocuments(modifiedQuery);
    }

    @Override
    public String getName() {
        return "Cosine similarity + relevance feedback";
    }

}
