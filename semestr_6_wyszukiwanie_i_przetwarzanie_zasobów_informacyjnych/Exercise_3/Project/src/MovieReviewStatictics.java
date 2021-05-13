import opennlp.tools.lemmatizer.DictionaryLemmatizer;
import opennlp.tools.namefind.NameFinderME;
import opennlp.tools.namefind.TokenNameFinderModel;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.stemmer.PorterStemmer;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import opennlp.tools.util.Span;

import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.text.DecimalFormat;
import java.util.*;
import java.util.logging.Level;
import java.util.logging.Logger;


public class MovieReviewStatictics {
    private static final String DOCUMENTS_PATH = "../movies/";
    private static final String LEMMATIZER_DICT = "../models/en-lemmatizer.dict";
    private static final String SENTENCE_MODEL = "../models/en-sent.bin";
    private static final String TOKENIZER_MODEL = "../models/en-token.bin";
    private static final String POST_MODEL_FILE = "../models/en-pos-maxent.bin";
    private static final String PEOPLE_MODEL_FILE = "../models/en-ner-person.bin";
    private static final String PLACES_MODEL_FILE = "../models/en-ner-location.bin";
    private static final String ORGANIZATION_MODEL_FILE = "../models/en-ner-organization.bin";
    private int _verbCount = 0;
    private int _nounCount = 0;
    private int _adjectiveCount = 0;
    private int _adverbCount = 0;
    private int _totalTokensCount = 0;

    private PrintStream _statisticsWriter;
    private SentenceModel _sentenceModel;
    private TokenizerModel _tokenizerModel;
    private DictionaryLemmatizer _lemmatizer;
    private PorterStemmer _stemmer;
    private POSModel _posModel;
    private TokenNameFinderModel _peopleModel;
    private TokenNameFinderModel _placesModel;
    private TokenNameFinderModel _organizationsModel;

    public static void main(String[] args) {
        MovieReviewStatictics statictics = new MovieReviewStatictics();
        statictics.run();
    }

    private void run() {
        try {
            initModelsStemmerLemmatizer();

            File dir = new File(DOCUMENTS_PATH);
            File[] reviews = dir.listFiles((d, name) -> name.endsWith(".txt"));

            _statisticsWriter = new PrintStream("statistics.txt", "UTF-8");

            Arrays.sort(reviews, Comparator.comparing(File::getName));
            for (File file : reviews) {
                System.out.println("Movie: " + file.getName().replace(".txt", ""));
                _statisticsWriter.println("Movie: " + file.getName().replace(".txt", ""));

                String text = new String(Files.readAllBytes(file.toPath()));
                processFile(text);

                _statisticsWriter.println();
            }

            overallStatistics();
            _statisticsWriter.close();

        } catch (IOException ex) {
            Logger.getLogger(MovieReviewStatictics.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private void initModelsStemmerLemmatizer() {
        try {
            File model = new File(LEMMATIZER_DICT);
            _lemmatizer = new DictionaryLemmatizer(model);
            _stemmer = new PorterStemmer();

            File sentenceFileModel = new File(SENTENCE_MODEL);
            _sentenceModel = new SentenceModel(sentenceFileModel);

            File tokenizerModelFile = new File(TOKENIZER_MODEL);
            _tokenizerModel = new TokenizerModel(tokenizerModelFile);

            File posModelFile = new File(POST_MODEL_FILE);
            _posModel = new POSModel(posModelFile);

            File peopleModelFile = new File(PEOPLE_MODEL_FILE);
            _peopleModel = new TokenNameFinderModel(peopleModelFile);

            File placesModelFile = new File(PLACES_MODEL_FILE);
            _placesModel = new TokenNameFinderModel(placesModelFile);

            File organizationModelFile = new File(ORGANIZATION_MODEL_FILE);
            _organizationsModel = new TokenNameFinderModel(organizationModelFile);
        } catch (IOException ex) {
            Logger.getLogger(MovieReviewStatictics.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private void processFile(String text) {
        // Sentences
        SentenceDetectorME sentenceDetectorME = new SentenceDetectorME(_sentenceModel);
        String[] sentences = sentenceDetectorME.sentDetect(text);
        int noSentences = sentences.length;

        // Tokenize
        TokenizerME tokenizerME = new TokenizerME(_tokenizerModel);
        String[] tokenize = tokenizerME.tokenize(text);

        // Clear "invalid" tokens
        List<String> tokensList = new LinkedList<>();
        for(String token : tokenize) {
            String updatedToken = token.toLowerCase().replaceAll("[^a-z0-9]", "");
            if(updatedToken.compareTo("") != 0)
                tokensList.add(updatedToken);
        }
        int noTokens = tokensList.size();
        _totalTokensCount += noTokens;

        // Prepare correct array of Strings
        String[] tokens = tokensList.toArray(new String[0]);

        // Tags
        POSTaggerME posTaggerME = new POSTaggerME(_posModel);
        String[] tags = posTaggerME.tag(tokens);

        // Stems
        Set<String> stems = new HashSet<>();
        for(String token : tokens) {
            stems.add(_stemmer.stem(token));
        }
        int noStemmed = stems.size();

        // Lemmatize
        Set<String> words = new HashSet<>();
        String[] lemmatizes = _lemmatizer.lemmatize(tokens, tags);
        for(String lemmatize : lemmatizes) {
            if(lemmatize.compareTo("O") != 0)
                words.add(lemmatize);
        }
        int noWords = words.size();

        // People
        NameFinderME peopleFinder = new NameFinderME(_peopleModel);
        Set<String> people = findData(peopleFinder, tokenize);

        // Organization
        NameFinderME organizationFinder = new NameFinderME(_organizationsModel);
        Set<String> organizations = findData(organizationFinder, tokenize);

        // Location
        NameFinderME locationFinder = new NameFinderME(_placesModel);
        Set<String> locations = findData(locationFinder, tokenize);

        // Compute POS tagging statistics:
        for(String tag : tags) {
            if(tag.startsWith("V"))
                _verbCount += 1;
            else if(tag.startsWith("J"))
                _adjectiveCount += 1;
            else if(tag.startsWith("N"))
                _nounCount += 1;
            else if(tag.startsWith("R"))
                _adverbCount += 1;
        }

        saveResults("Sentences", noSentences);
        saveResults("Tokens", noTokens);
        saveResults("Stemmed forms (unique)", noStemmed);
        saveResults("Words from a dictionary (unique)", noWords);

        saveNamedEntities("People", people);
        saveNamedEntities("Locations", locations);
        saveNamedEntities("Organizations", organizations);
    }

    private Set<String> findData(NameFinderME finderME, String[] tokens) {
        Set<String> result = new HashSet<>();
        Span[] spans = finderME.find(tokens);
        for(Span span : spans) {
            int start = span.getStart();
            int end = span.getEnd();
            StringBuilder name = new StringBuilder();
            for(int i = start; i < end; i++) {
                name.append(tokens[i]).append(" ");
            }
            result.add(name.toString().trim());
        }

        return result;
    }

    private void saveResults(String feature, int count) {
        String s = feature + ": " + count;
        System.out.println("   " + s);
        _statisticsWriter.println(s);
    }

    private void saveNamedEntities(String entityType, Set<String> values) {
        StringBuilder s = new StringBuilder(entityType + ": ");
        for(String value : values) {
            s.append(value).append("  ");
        }
        String record = s.toString().trim().replaceAll("  ", ", ");

        System.out.println("   " + record);
        _statisticsWriter.println(record);
    }

    private void overallStatistics() {
        _statisticsWriter.println("---------OVERALL STATISTICS----------");
        DecimalFormat f = new DecimalFormat("#0.00");

        if (_totalTokensCount == 0) _totalTokensCount = 1;
        String verbs = f.format(((double) _verbCount * 100) / _totalTokensCount);
        String nouns = f.format(((double) _nounCount * 100) / _totalTokensCount);
        String adjectives = f.format(((double) _adjectiveCount * 100) / _totalTokensCount);
        String adverbs = f.format(((double) _adverbCount * 100) / _totalTokensCount);

        _statisticsWriter.println("Verbs: " + verbs + "%");
        _statisticsWriter.println("Nouns: " + nouns + "%");
        _statisticsWriter.println("Adjectives: " + adjectives + "%");
        _statisticsWriter.println("Adverbs: " + adverbs + "%");

        System.out.println("---------OVERALL STATISTICS----------");
        System.out.println("Adverbs: " + adverbs + "%");
        System.out.println("Adjectives: " + adjectives + "%");
        System.out.println("Verbs: " + verbs + "%");
        System.out.println("Nouns: " + nouns + "%");
    }

}
