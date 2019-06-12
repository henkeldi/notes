
# Speech Recognizer

AndroidManifest.xml
```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

MyVoiceListener.kt

```kotlin
class MyVoiceListener() : RecognitionListener {

    override fun onPartialResults(results: Bundle?) {
        // Show partial result
        val data = results!!.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
        if (data != null && data.isNotEmpty()) {
            // Your code here for displaying partial results which is in data[0]
        }
    }

    // STEP 4: Process the final result
    override fun onResults(results: Bundle?) {
        val data = results!!.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
        if (data != null && data.isNotEmpty()) {
            val confidence = results.getFloatArray(SpeechRecognizer.CONFIDENCE_SCORES)
            // Highest confidence result in data[0] with score confidence[0]
            
            // Optional: loop through other results
            if(data.size > 1) {
                for (i in 1 until data.size) {
                    // Other results
                }
            }
        }
    }
    
    override fun onRmsChanged(level: Float) {
        // Your code here for displaying noise level change
    }
}
```

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    // STEP 5 Request permission and initiate speech recognizer
    voiceListener = MyVoiceListener()
    speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
    speechRecognizer.setRecognitionListener(voiceListener)
    
    // STEP 6: Create an recognize intent
    speakIntent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        .putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        .putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, "com.example.speechrecognize") 
        .putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
        .putExtra(RecognizerIntent.EXTRA_LANGUAGE, "en")
        
        
    val audioManager = getSystemService(Context.AUDIO_SERVICE) as AudioManager
    speechRecognizer.startListening(speakIntent)

    // audioManager.adjustStreamVolume(AudioManager.STREAM_MUSIC, AudioManager.ADJUST_UNMUTE, 0)
    audioManager.adjustStreamVolume(AudioManager.STREAM_MUSIC, AudioManager.ADJUST_MUTE, 0)
}
```

# Source

[What’s New in Android Machine Learning](https://www.youtube.com/watch?v=wpKJpeOy-68)