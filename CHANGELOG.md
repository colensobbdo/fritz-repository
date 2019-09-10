Change Log
==========

`Fritz` follows [Semantic Versioning](http://semver.org/)

---

## [4.0.0]

In the latest release, we've several improvements listed below.

This repo on github moving forward will be deprecated in favor of hosting our SDK in a new maven repository:

Change:

maven {
    url 'https://raw.github.com/fritzlabs/fritz-repository/master'
}

To:

maven {
    url "https://fritz.mycloudrepo.io/public/repositories/android"
}

Changes
* Adding support for model variants (fast, accurate, small)
* Removing deprecated methods for the result classes.
* 2x speed improvement for image processing with Renderscript.
* Adding TFL support for CPU threads, GPU Delegate, and NNAPI
* Improved rendering on Surface views
* Improve segmentation blend mode (hair coloring)

Migrating from 3.x.x to 4.x.x

**Core**
* Image rotation is now an enum.

```
// Old version
int imgRotation = FritzVisionOrientation.getImageRotationFromCamera(this, cameraId);
FritzVisionImage visionImage = FritzVisionImage.fromBitmap(bitmap, imgRotation);

// Change
ImageRotation imageRotation = FritzVisionOrientation.getImageRotationFromCamera(this, cameraId);
FritzVisionImage visionImage = FritzVisionImage.fromBitmap(bitmap, imageRotation);
```

**FritzVision**

- Add RenderScript support to your app
```
// In your app/build.gradle

android {
    defaultConfig {
        renderscriptTargetApi 21
        renderscriptSupportModeEnabled true
    }
}
```

- For any of the predictor options, you can now declare option in the following way:

```
// Old
FritzVisionSegmentPredictorOptions options = FritzVisionSegmentPredictorOptions.Builder()
    .targetConfidenceScore(.3f);
    .build();
    
// New
FritzVisionSegmentPredictorOptions options = FritzVisionSegmentPredictorOptions();
options.confidenceThreshold = .3f;
```

**Image Segmentation**

* Renaming Classes ("Segment" -> "Segmentation"):
    - FritzVisionSegmentPredictor -> FritzVisionSegmentationPredictor
    - FritzVisionSegmentResult -> FritzVisionSegmentationResult
    - FritzVisionSegmentPredictorOptions -> FritzVisionSegmentationPredictorOptions
    - MaskType -> MaskClass

* Model dependencies:
    * Sky Segmentation:
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-sky-segmentation-model-fast:4.x.x"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new SkySegmentationManagedModelFast();
              ```
    * Pet Segmentation
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-pet-segmentation-model-fast:4.x.x"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new PetSegmentationManagedModelFast();
              ```
     * Hair Segmentation
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-hair-segmentation-model-fast:4.x.x"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new HairSegmentationManagedModelFast();
              ```
     * Living Room Segmentation
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-living-room-segmentation-model-fast:4.x.x"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new LivingRoomSegmentationManagedModelFast();
              ```
     * Outdoor Segmentation
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-outdoor-segmentation-model-fast:4.x.x"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new OutdoorSegmentationManagedModelFast();
              ```
     * People Segmentation
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-people-segmentation-model-fast:4.x.x"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new PeopleSegmentationManagedModelFast();
              ```
        * Accurate Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-people-segmentation-model-accurate:4.x.x"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new PeopleSegmentationManagedModelAccurate();
              ```
        * Small Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-people-segmentation-model-small:4.x.x"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new PeopleSegmentationManagedModelSmall();
              ```
* Blend Mode:

Alpha value is specified on the created mask. The class ``BlendModeType`` is removed.
```
// Old
BlendMode blendMode = BlendModeType.SOFT_LIGHT.create();
Bitmap maskBitmap = hairResult.buildSingleClassMask(MaskType.HAIR, blendMode.getAlpha(), 1, options.getTargetConfidenceThreshold(), maskColor);
Bitmap blendedBitmap = visionImage.blend(maskBitmap, blendMode);

// New
BlendMode blendMode = BlendMode.SOFT_LIGHT;
Bitmap maskBitmap = hairResult.buildSingleClassMask(MaskClass.HAIR, 180, 1, options.confidenceThreshol, maskColor);
Bitmap blendedBitmap = visionImage.blend(maskBitmap, blendMode);
```


## [2.0.0]

In the latest release, we've made it easier to access and draw your prediction results to a canvas. For the full API documentation, please visit: https://docs.fritz.ai/android/2.0.0/reference/packages.html.

Changes:

1. Create result classes for each predictor
2. Simplify SDK initialization
3. Rename a couple of modules (vision-label-model -> vision-label)
4. Move Bitmap helpers to BitmapUtils class
5. Use a CustomModel class instead of ModelSettings
6. Rename model management service to FritzCustomModelService
7. Use app context provided during Fritz.configure
8. Ability to create separate interpreters for predictors

#### To Migrate from 1.x.x to 2.0.0

There are several breaking changes from this release:

- Module renaming - In your app/build.gradle file, change these module names

Previous module names
```
dependencies {
    // Image Labeling
    implementation "ai.fritz:vision-label-model:1.x.x"

    // Object Detection
    implementation "ai.fritz:vision-object-model:1.x.x"

    // Image Segmentation
    implementation "ai.fritz:vision-people-segment-model:1.x.x"
    implementation "ai.fritz:vision-living-room-segment-model:1.x.x"
    implementation "ai.fritz:vision-outdoor-segment-model:${sdk_version}:1.x.x"
}
```

to

```
dependencies {
    // Image Labeling
    implementation "ai.fritz:vision-label:1.x.x"

    // Object Detection
    implementation "ai.fritz:vision-object:1.x.x"

    // Image Segmentation
    implementation "ai.fritz:vision-people-segment:1.x.x"
    implementation "ai.fritz:vision-living-room-segment:1.x.x"
    implementation "ai.fritz:vision-outdoor-segment:${sdk_version}:1.x.x"
}
```

- All FritzVisionPredictor's predict method now methods now return a ```FritzVisionResult``` object.

Previously for object detection
```
List<FritzVisionObject> visionObjects = objectPredictor.predict(fritzVisionImage);
```

To
```
FritzVisionObjectResult objectResult = objectPredictor.predict(fritzVisionImage);
List<FritzVisionObject> visionObjects = objectResult.getVisionObjects();
```

These classes have helper classes such as ```drawBoundingBoxes``` and ```drawVisionImage``` for your convenience.

Please refer to the documentation to see the appropriate changes for each feature: https://docs.fritz.ai/

- FritzVisionImage methods to manipulate bitmaps (scale, centerCrop, resize, etc) are now accessed in BitmapUtils.

Previously

```
Bitmap resizedBitmap = FritzVisionImage.resize(image.getBitmap(), INPUT_SIZE, INPUT_SIZE);
```

To:
```
Bitmap resizedBitmap = BitmapUtils.resize(image.getBitmap(), INPUT_SIZE, INPUT_SIZE);
```

- For custom model management, change the Job Service name in AndroidManifest.xml

Previously
```
<service
    android:name="ai.fritz.core.FritzJob"
    android:exported="true"
    android:permission="android.permission.BIND_JOB_SERVICE" />
```

To
```
<service
    android:name="ai.fritz.core.FritzCustomModelService"
    android:exported="true"
    android:permission="android.permission.BIND_JOB_SERVICE" />
```

- For those of you using custom models, ModelSettings is now deprecated in favor of a CustomModel class.

Previously
```

FritzTFLiteInterpreter.create(new ModelSettings.Builder()
    .modelId("modelId")
    .modelPath("mnist.tflite")
    .modelVersion(1).build());
)
```

To:
```

FritzTFLiteInterpreter.create(new MnistCustomModel());
)
```

To download the class for your model, please visit the webapp and under Custom Model > Your Model > SDK Instructions.


- Removed singletons for predictors that developers can allocate separate interpreters.

Previously
```
    FritzVisionObjectPredictor predictor = FritzVisionObjectPredictor.getInstance(this, options);
```

To:
```
    FritzVisionObjectPredictor predictor = new FritzVisionObjectPredictor();
```

## [1.4.0](https://github.com/fritzlabs/swift-framework/releases/tag/1.4.0)

1. Allowing the ability to add a custom style transfer model

