
# Audio

*Audio Programming is "hard real-time" programming*

Latency:
    < 10ms: good for interactive audio performance
    10-30 ms: noticable

Audio APIs

* CoreAudio
* DirectSound
* WASAPI
* ASIO
* ALSA
* JACK
* OpenSL ES

Audio data representation

* float in range from [-1, 1]
* Audio API gives you a buffer. Typically in a callback. Typically 32 - 1024 Samples at a time

```c++
void audioCallback(float** channelData,
                   int numChannels,
                   int numSamples) {
    
    for (int channel = 0; channel < numChannels; ++channel) {
        for (int sample = 0; sample < numSamples; ++sample>) {
            channelData[channel][sample] = ... // Perform DSP calculations here
        }
    }
}
```

# Do's and Dont's

* Don't block on the audio thread
* Don't call anything that blocks / waits
* Dont't call new or delete
* Lock your real-time data into memory prevent page-outs (mlock(), munlock() on POSIX systems)

# GUI -> Audio thread communnication

```c++
class Synthesiser {
    public:
        Synthesiser() : level_(1.0f) {}
    
    // GUI thread:
    void levelChanged(float newValue) {
        level.store(newValue);
    }
    private:
        // Audio thread
    void audioCallback(float* buffer, int numSamples) noexcept {
        for (int i = 0; i < numSamples; ++i) {
            buffer[i] = level.load() * getNextAudioSample();
        }
    }
    std::atomic<float> level;
}
```

# Audio thread -> GUI communnication

```c++
class Synthesiser {

    void audioCallback(float* buffer, int numSamples) noexcept {
        parameter.store(newValue);
        guiUpToDate.store(false);
    }

    std::atomic<float> parameter;
    std::atomic<bool> guiUpToDate;

    void timerCallback() { // called 30x / second on a low priority thread
        if (guiUpToDate.compare_exchange_strong(false, true)) {
            updateGui(parameter.load());
        }
    }
}
```

# Audio thread -> GUI communnication for more compliacted types

```c++
class Synthesiser {

    void audioCallback(float* buffer, int numSamples) noexcept {
        std::shared_ptr<Widget> widgetToUse = std::atomic_load(&currentWidget);
        // do something with widgetToUse...
    }

    void updateWidget( /* args */) {
        std::shared_ptr<Widget> newWidget = std::make_shared<Widget>(/* args */);
        releasePool.add(newWidget);
        std::atomic_store(&currentWidget, newWidget);
    }

    std::shared_ptr<Widget> currentWidget;
    ReleasePool releasePool;
}
```

# Source

* [CppCon 2015: Timur Doumler “C++ in the Audio Industry”](https://www.youtube.com/watch?v=boPEO2auJj4)