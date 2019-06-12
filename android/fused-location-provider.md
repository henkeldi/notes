
# Fused Location Provider

AndroidManifest.xml
```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
```

MyActivity.kt

```kotlin
private lateinit var fusedLocationClient: FusedLocationProviderClient
private lateinit var locationRequest: LocationRequest
private lateinit var locationCallback: LocationCallback

override fun onCreate(savedInstanceState: Bundle?) {
    fusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
    
    locationRequest = LocationRequest.create().apply {
        setInterval(5000)
        setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY)    
    }
    
    locationCallback = object: LocationCallback() {
        override fun onLocationResult(locationResult:LocationResult) {
            // ...
        }
    }
}

override fun onResume() {
    super.onResume()
    fusedLocationClient.requestLocationUpdates(
        locationRequest,
        locationCallback,
        null /* Looper */
    )
}

override fun onPause() {
    super.onPause()
    fusedLocationClient.removeLocationUpdates(locationCallback)
}
```

