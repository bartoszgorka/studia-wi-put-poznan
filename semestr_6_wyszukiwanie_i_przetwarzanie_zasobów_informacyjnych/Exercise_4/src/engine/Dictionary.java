package engine;

import opennlp.tools.stemmer.PorterStemmer;

import java.util.*;

public class Dictionary {
    public ArrayList<String> _keywords;
    public ArrayList<String> _terms;
    public HashMap<String, String> _termsToKeywords;
    public ArrayList<Double> _idf;

    public HashMap<String, Integer> _termID;

    public Dictionary(int capacity) {
        this._keywords = new ArrayList<>(capacity);
    }

    public void computeIDFs(ArrayList<Document> documents) {
        _idf = new ArrayList<>(_terms.size());
        double documentsSize = (double) documents.size();

        for (int i = 0; i < _terms.size(); i++) {
            int counter = 0;
            for (Document document : documents) {
                if (document._terms.contains(_terms.get(i))) {
                    counter++;
                }
            }


            double log = 0.0d;
            if (counter > 0) {
                log = Math.log(documentsSize / (double) counter);
            }

            _idf.add(i, log);
        }

        // 1) iterate over the _terms DONE
        // 2) check how many documents contain this term (document._terms.contains()) DONE
        // 3) compute idf value (Math.log()) and update _idf vector (add idf value) DONE
    }

    public void doProcessing(PorterStemmer stemmer, boolean log) {
        Set<String> stemmed = new HashSet<>();
        _termsToKeywords = new HashMap<>(_keywords.size());
        _terms = new ArrayList<>(_keywords.size());
        for (String s : _keywords) {
            String stem = stemmer.stem(s);
            stemmed.add(stem);
            _termsToKeywords.put(stem, s);
        }

        _terms.addAll(stemmed);
        Collections.sort(_terms);

        _termID = new HashMap<>();
        for (int i = 0; i < _terms.size(); i++)
            _termID.put(_terms.get(i), i);

        if (log) {
            for (String s : _terms)
                System.out.println(s);
            System.out.println(_terms.size() + " " + _keywords.size());
        }
    }

    void print() {
        for (int i = 0; i < _terms.size(); i++) {
            System.out.println(i + " : " + _terms.get(i) + "   idf = " + _idf.get(i));
        }
    }
}
