
# Camera X

MyAnalyzer.kt

```kotlin
// Step 1: Create an Analyzer
class MyAnalyzer : ImageAnalysis.Analyzer {
    
    override fun analyze(image: ImageProxy, rotationDegrees: Int) {
        // Your Machine Learning Code here!
    }
}
```

CameraFragment.kt

```kotlin
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    // Step 2: Create an Analyzer Config
    val analyzerConfig = ImageAnalysisConfig.Builder().apply {
        val analyzerThread = HandlerThread("MyAnalysis").apply {
            start()
        }
        setCallbackHandler(Handler(analyzerThread.looper))
        // Analyze latest image rather than *every* image
        setImageReaderMode(ImageAnalysisUseCase.ImageReaderMode.ACQUIRE_LATEST_IMAGE)
    }.build()
    
    // Step 3: Apply declared config to CameraX using the same lifecycle owner
    val analyzerUseCase = ImageAnalysis(analyzerConfig).apply {
        analyzer = MyAnalyzer()
    }
    
    // STEP 4: Bind to the Lifecycle owner, e.g. AppCompatActivity, Fragment, etc.
    CameraX.bindToLifecycle(this, analyzerUseCase)
}
```

