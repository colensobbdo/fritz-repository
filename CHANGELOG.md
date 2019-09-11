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
* Adding support for model variants (fast, accurate, small) so you can build the perfect experience for your users. 
     - Fast models are optimized for runtime performance with an accuracy tradeoff. This should be used in cases where model predictions need to happen quickly (e.g video processing, live preview, etc). This comes with a tradeoff in accuracy.
     - Accurate models are optimized to display the best model prediction with a speed tradeoff. This should be used in cases where you're dealing with still images (i.e photo editing)
     - Small models are optimized for model size at the cost of accuracy. This should be used in cases where developers are cautious of bloating their apps with models.
* Models now have their own versioning system separate from the SDK and follow semantic versioning. This enables Fritz to release new versions of models without changing any existing user experiences.
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
    * The libraries for models are now on separate versions, allowing for individual updates and releases on when new improvements are made. As of the release, all models are now currently on version 1.0.0.
    * Sky Segmentation:
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-sky-segmentation-model-fast:1.0.0"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new SkySegmentationManagedModelFast();
              ```
    * Pet Segmentation
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-pet-segmentation-model-fast:1.0.0"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new PetSegmentationManagedModelFast();
              ```
     * Hair Segmentation
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-hair-segmentation-model-fast:1.0.0"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new HairSegmentationManagedModelFast();
              ```
     * Living Room Segmentation
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-living-room-segmentation-model-fast:1.0.0"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new LivingRoomSegmentationManagedModelFast();
              ```
     * Outdoor Segmentation
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-outdoor-segmentation-model-fast:1.0.0"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new OutdoorSegmentationManagedModelFast();
              ```
     * People Segmentation
        * Fast Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-people-segmentation-model-fast:1.0.0"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new PeopleSegmentationManagedModelFast();
              ```
        * Accurate Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-people-segmentation-model-accurate:1.0.0"
              ```
            * Downloading it OTA:
              ```
                FritzManagedModel managedModel = new PeopleSegmentationManagedModelAccurate();
              ```
        * Small Variant
            * Including it on device (in app/build.gradle):
              ```
                implementation "ai.fritz:vision-people-segmentation-model-small:1.0.0"
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

## [3.0.0]

In the latest release, we've several improvements listed below. For the full API documentation, please visit: https://docs.fritz.ai/android/3.0.0/reference/packages.html.

## Changes:

1. Simplify dependencies
2. Allow for lazy loading models with a FritzManagedModel class.
3. Saved on-device models stored as a FritzOnDeviceModel
4. Download models by tags (configured in the webapp)
5. Model tags + metadata

## To Migrate from 2.x.x to 3.0.0

**Module renaming - In your app/build.gradle file, change these module names**

**2.x.x**
```
dependencies {
    // Image Labeling
    implementation "ai.fritz:vision-label:2.x.x"

    // Object Detection
    implementation "ai.fritz:vision-object:2.x.x"

    // Style Transfer
    implementation "ai.fritz:vision-style-paintings:2.x.x"

    // Image Segmentation
    implementation "ai.fritz:vision-people-segment:2.x.x"
    implementation "ai.fritz:vision-living-room-segment:2.x.x"
    implementation "ai.fritz:vision-outdoor-segment:2.x.x"
}
```

**3.x.x**

```
dependencies {
    // Image Labeling
    implementation "ai.fritz:vision-image-label-model:3.x.x"

    // Object Detection
    implementation "ai.fritz:vision-object-detection-model:3.x.x"

    // Style Transfer
    implementation "ai.fritz:vision-style-painting-models:3.x.x"

    // Image Segmentation
    implementation "ai.fritz:vision-people-segmentation-model:3.x.x"
    implementation "ai.fritz:vision-living-room-segmentation-model:3.x.x"
    implementation "ai.fritz:vision-outdoor-segmentation-model:3.x.x"
}
```

Several dependencies have been removed and the functionality is now in FritzVision

- ai.fritz:style-base
- ai.fritz:image-segmentation


**Using FritzManagedModel and FritzOnDeviceModel**

In order to provide lazy loading models, we've created 2 separate classes to define models loaded
into Vision predictors and Custom Model intepreters: FritzManagedModel and FritzOnDeviceModel.

Why we made this change?
- Decrease initial app size through lazy loading - Allow developers to manage their app size and download models over the air.
- Simplify the dependency chain - Allow developers to use only the FritzCore + FritzVision dependency in order to get started.
- Use Custom Models with the Vision API- Developers can use custom models with the existing Vision API by plugging it into an existing predictor (e.g ObjectDetection). We provide model training templates that you can use on your own training data.

**2.x.x** - You would define a predictor like so:
```
FritzVisionObjectPredictor objectPredictor = new FritzVisionObjectPredictor();
FritzVisionObjectResult objectResult = objectPredictor.predict(fritzVisionImage);
List<FritzVisionObject> visionObjects = objectResult.getVisionObjects();
```

**3.x.x** - You have 2 options of including a model for on-device inference:

1. **Include it directly in your app build.** This increases your app size but your users will be able to access
the model immediately once they download it from the app store.
    
    **Using a Vision Predictor with a FritzOnDeviceModel:**
    ```
    FritzOnDeviceModel onDeviceModel = new ObjectDetectionOnDeviceModel();
    FritzVisionObjectPredictor predictor = FritzVision.ObjectDetection.getPredictor();
    ```

    **Using a Custom Model with a FritzOnDeviceModel:**
    ```
    String modelPath = "<PATH TO YOUR MODEL FILE STORED IN THE ASSETS FOLDER>";
    String modelId = "<YOUR MODEL ID>";
    int modelVersion = 1;
    FritzOnDeviceModel onDeviceModel = new FritzOnDeviceModel(modelPath, modelId, modelVersion);
    FritzTFLiteInterpreter tflite = new FritzTFLiteInterpreter(onDeviceModel);
    ```

2. **Lazy load the model the first time the app launches.** This reduces your initial app size when your users install it from the store, but you will have to handle the experience before the model is loaded onto the device.
    
    **Lazy loading a Vision Predictor:**
    ```
    // Global predictor variable
    FritzVisionObjectPredictor predictor;

    // Load your predictor
    FritzManagedModel managedModel = new ObjectDetectionManagedModel();
    FritzVision.ObjectDetection.loadPredictor(managedModel, new PredictorStatusListener<FritzVisionObjectPredictor>() {
        @Override
        public void onPredictorReady(FritzVisionObjectPredictor objectPredictor) {
            predictor = objectPredictor;
        }
    });

    // Manage access to specific features and check if the predictor is ready to use.
    if(predictor != null) {
        predictor.predict(...);
    }
    ```

    **Lazy loading a Custom Model**
    ```
    FritzManagedModel managedModel = new FritzManagedModel("<YOUR MODEL ID>");
    FritzModelManager modelManager = new FritzModelManager(managedModel);
    modelManager.loadModel(new ModelReadyListener() {
        @Override
        public void onModelReady(FritzOnDeviceModel onDeviceModel) {
            tflite = new FritzTFLiteInterpreter(onDeviceModel);
            Log.d(TAG, "Interpreter is now ready to use");
        }
    });
    ```

**Vision API changes**

**2.x.x** - Initialize the predictor directly
```
FritzVisionObjectPredictor objectPredictor = new FritzVisionObjectPredictor(options);
FritzVisionStylePredictor stylePredictor = new FritzVisionStylePredictor(options);
FritzVisionLabelPredictor labelPredictor = new FritzVisionLabelPredictor(options);
FritzVisionSegmentPredictor segmentPredictor = new FritzVisionSegmentPredictor(options);
```

**3.x.x** - Accessing Vision Predictors with a loaded model (a class that extends FritzOnDeviceModel) to use immediately.
```
FritzVisionObjectPredictor objectPredictor = FritzVision.ObjectDetection.getPredictor(onDeviceModel, options);
FritzVisionStylePredictor stylePredictor = FritzVision.StyleTransfer.getPredictor(onDeviceModel, options);
FritzVisionLabelPredictor labelPredictor = FritzVision.ImageLabeling.getPredictor(onDeviceModel, options);
FritzVisionSegmentPredictor segmentPredictor = FritzVision.ImageSegmentation.getPredictor(onDeviceModel, options);
```

## New Features in 3.0.0

- [Pose Estimation](https://docs.fritz.ai/develop/vision/pose-estimation/android.html)
- [Tag + Metadata](https://docs.fritz.ai/develop/custom-models/tag-based/android.html)
- [Custom Models with the Vision API](https://docs.fritz.ai/develop/vision/style-transfer/android.html#how-to-customize)


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

