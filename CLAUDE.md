# CLAUDE.md - Kinect Toolbox (ktb) Project Context

## Project Overview
**kinect-toolbox (ktb)** is a high-level Python wrapper for pylibfreenect2 that provides a more intuitive, "OpenCV-like" interface for the Microsoft Kinect v2. It abstracts away the complex C++ paradigms of libfreenect2 and presents a simple, pythonic API for common Kinect operations.

## Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                  Kinect Toolbox (ktb)                       │
│  High-level Python wrapper with OpenCV-like interface       │
├─────────────────────────────────────────────────────────────┤
│                    pylibfreenect2                           │
│     Python bindings for libfreenect2 (Cython-based)        │
├─────────────────────────────────────────────────────────────┤
│                    libfreenect2                             │
│  C++ library with GPU acceleration (CUDA/OpenCL/OpenGL)     │
├─────────────────────────────────────────────────────────────┤
│                Microsoft Kinect v2                          │
│            USB 3.0 depth + color camera                     │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Philosophy
**"Make Kinect v2 work like cv2.VideoCapture()"**
- Simple instantiation: `k = ktb.Kinect()`
- Frame capture loop: `frame = k.get_frame(ktb.COLOR)`
- Multiple frame types with consistent API
- Automatic pipeline selection and fallback
- Built-in registration and undistortion

## Core Components

### 1. **ktb/kinect.py** - Main Kinect Class
**Purpose**: Central interface for all Kinect operations
**Key Features**:
- Device enumeration and connection management
- Automatic pipeline selection (OpenGL/OpenCL based on headless mode)
- Frame capture with multiple types
- Point cloud generation with real-world coordinates
- Video recording capabilities
- Camera parameter management

**Key Methods**:
```python
# Basic usage
k = ktb.Kinect()                          # Auto-detect and connect
frame = k.get_frame(ktb.COLOR)            # Get registered color frame
frames = k.get_frame([ktb.COLOR, ktb.DEPTH])  # Multiple frames

# Advanced usage
k = ktb.Kinect(headless=True, pipeline=CudaPacketPipeline())
ptcld = k.get_ptcld(colorized=True)       # 3D point cloud with colors
k.record("video.avi", ktb.RAW_COLOR)      # Record video
```

### 2. **ktb/constants.py** - Frame Type Constants
**Purpose**: Defines frame type enumeration for cleaner API
```python
COLOR = 0      # 512x424 registered color (RGB)
DEPTH = 1      # 512x424 undistorted depth (mm)
IR = 2         # 512x424 infrared
RAW_COLOR = 3  # 1920x1080 raw color (BGR)
RAW_DEPTH = 4  # 512x424 raw depth (mm)
```

### 3. **ktb/utils.py** - Utility Classes
**Purpose**: Helper classes for internal use
- `dotdict`: Dictionary with dot-notation access for camera parameters

### 4. **ktb/__init__.py** - Package Interface
**Purpose**: Main package imports and environment validation
- Imports core classes and constants
- Validates LIBFREENECT2_INSTALL_PREFIX environment variable
- Provides import warnings for missing configuration

## Frame Types and Data Flow

### Frame Processing Pipeline
```
Raw Kinect Data → pylibfreenect2 → ktb Processing → Output
     ↓                ↓               ↓             ↓
USB 3.0 → Color/Depth/IR → Registration → numpy arrays
```

### Frame Type Details
| Type | Dimensions | Format | Description | Use Case |
|------|------------|--------|-------------|----------|
| `RAW_COLOR` | 1920×1080 | BGR | Original color resolution | High-res photography |
| `RAW_DEPTH` | 512×424 | uint16 (mm) | Raw depth data | Direct sensor access |
| `COLOR` | 512×424 | RGB | Color registered to depth | Computer vision |
| `DEPTH` | 512×424 | float32 (mm) | Undistorted depth | 3D reconstruction |
| `IR` | 512×424 | uint16 | Infrared intensity | Night vision, tracking |

## Pipeline Management

### Automatic Pipeline Selection
```python
# ktb automatically selects optimal pipeline:
if headless:
    pipeline = OpenCLPacketPipeline()  # Server/headless environments
else:
    pipeline = OpenGLPacketPipeline()  # Desktop with display

# Manual override supported:
k = ktb.Kinect(pipeline=CudaPacketPipeline())  # Force CUDA
```

### Pipeline Performance Hierarchy
1. **CudaPacketPipeline** - 25-35 FPS (NVIDIA only, best performance)
2. **OpenCLPacketPipeline** - 20-30 FPS (Cross-platform GPU)
3. **OpenGLPacketPipeline** - 15-25 FPS (Graphics acceleration)
4. **CpuPacketPipeline** - 5-15 FPS (CPU fallback, always works)

## Camera Calibration and 3D Processing

### Intrinsic Parameters
```python
k = ktb.Kinect()
params = k.intrinsic_parameters  # dotdict access
print(f"Focal length: fx={params.fx}, fy={params.fy}")
print(f"Principal point: cx={params.cx}, cy={params.cy}")

# Modify parameters
params.fx = 366.193  # Custom calibration
```

### Extrinsic Parameters (World Positioning)
```python
k.position.z = 0.810        # Height above ground (meters)
k.position.elevation = -34  # Tilt angle (degrees)
k.position.azimuth = 0      # Pan angle (degrees)
```

### Point Cloud Generation
```python
# Basic point cloud (XYZ coordinates)
ptcld = k.get_ptcld()                    # Shape: (424, 512, 3)

# Colorized point cloud with RGB data
ptcld, colors = k.get_ptcld(colorized=True)

# ROI extraction
roi_ptcld = k.get_ptcld(roi=[100, 100, 200, 200])  # [y, x, h, w]

# Scale adjustment (default: mm, scale=1000 for meters)
ptcld_meters = k.get_ptcld(scale=1000)
```

## Dependencies and Compatibility

### Core Dependencies
```
numpy                 # Numerical computing
pylibfreenect2==0.1.3 # Original version (needs upgrade)
opencv-python>=4.2.0  # Computer vision
```

### Python Version Support
- **Current**: Python >= 3.6 (original design)
- **Target**: Python 3.10+ compatibility (requires pylibfreenect2-py310)

### Platform Support
- **Primary**: Ubuntu 18.04+ (tested)
- **Target**: Windows 10/11, macOS (untested)

## Integration with pylibfreenect2-py310

### Current Issues
1. **Version Dependency**: Hard-coded to `pylibfreenect2==0.1.3`
2. **Python 3.10+ Incompatibility**: Uses deprecated APIs
3. **Import Statements**: Direct pylibfreenect2 imports need updates

### Required Updates for Python 3.10+ Compatibility
```python
# OLD (requirements.txt)
pylibfreenect2==0.1.3

# NEW (requirements.txt)
pylibfreenect2-py310>=0.1.6

# OLD (kinect.py imports)
from pylibfreenect2 import Freenect2, SyncMultiFrameListener

# NEW (kinect.py imports) - no changes needed
# pylibfreenect2-py310 maintains same API
```

## Error Handling and Diagnostics

### Environment Validation
```python
# ktb/__init__.py automatically validates:
if (os.getenv('LIBFREENECT2_INSTALL_PREFIX') is None):
    warnings.warn("LIBFREENECT2_INSTALL_PREFIX environment variable not set")
```

### Device Detection
```python
# Automatic error handling in kinect.py
num_devices = self.fn.enumerateDevices()
if (num_devices == 0):
    raise RuntimeError('No device connected!')
if (device_index >= num_devices):
    raise RuntimeError('Device {} not available!'.format(device_index))
```

### Pipeline Fallback
```python
# Static method for safe pipeline import
def _import_pipeline(headless=False):
    if headless:
        return OpenCLPacketPipeline()  # GPU for headless
    else:
        return OpenGLPacketPipeline()  # GPU with display
```

## Usage Examples

### Basic Frame Capture
```python
import cv2
import ktb

k = ktb.Kinect()
while True:
    frame = k.get_frame(ktb.COLOR)  # 512x424 registered color
    cv2.imshow('Kinect', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

### Multi-Modal Capture
```python
import ktb

k = ktb.Kinect()
while True:
    color, depth, ir = k.get_frame([ktb.COLOR, ktb.DEPTH, ktb.IR])
    
    # Process frames...
    print(f"Depth range: {depth.min():.1f} - {depth.max():.1f} mm")
```

### 3D Point Cloud Visualization
```python
import ktb
import open3d as o3d

k = ktb.Kinect()
ptcld, colors = k.get_ptcld(colorized=True, scale=1000)  # meters

# Convert to Open3D format
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(ptcld.reshape(-1, 3))
pcd.colors = o3d.utility.Vector3dVector(colors)
o3d.visualization.draw_geometries([pcd])
```

### Server/Headless Operation
```python
import ktb

# Run on server without display
k = ktb.Kinect(headless=True)  # Uses OpenCL pipeline
data = []

for i in range(100):
    frame = k.get_frame(ktb.DEPTH)
    data.append(frame)
    print(f"Captured frame {i+1}/100")

# Save data for later processing
import numpy as np
np.save('kinect_depth_sequence.npy', np.array(data))
```

## Performance Optimization

### Pipeline Selection Strategy
```python
# For maximum performance (NVIDIA GPU required):
from pylibfreenect2 import CudaPacketPipeline
k = ktb.Kinect(pipeline=CudaPacketPipeline())

# For compatibility (works on most systems):
k = ktb.Kinect(headless=False)  # Uses OpenGL

# For servers (no display required):
k = ktb.Kinect(headless=True)   # Uses OpenCL
```

### Memory Management
```python
# ktb handles Frame object cleanup automatically
frames = k.get_frame([ktb.COLOR, ktb.DEPTH])
# Frames are copied to numpy arrays, original Frame objects released

# For point clouds, consider ROI to reduce memory:
ptcld = k.get_ptcld(roi=[50, 50, 300, 300])  # Process subset only
```

## Testing and Validation

### Quick Test (test.py)
```python
import cv2
import ktb

k = ktb.Kinect()
while True:
    color_frame = k.get_frame()
    cv2.imshow('frame', color_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

### Integration Test Strategy
1. **Device Detection**: `ktb.Kinect()` should not raise RuntimeError
2. **Frame Capture**: All frame types should return valid numpy arrays
3. **Pipeline Performance**: Benchmark different pipelines
4. **Point Cloud**: Verify 3D coordinates are reasonable
5. **Registration**: Check color-depth alignment quality

## Known Issues and Limitations

### Current Limitations
1. **No CUDA Support**: Only OpenGL/OpenCL pipelines supported
2. **Linux-Only Testing**: Windows/macOS untested
3. **Hard Dependencies**: Requires specific pylibfreenect2 version
4. **Limited Error Recovery**: Pipeline failures not gracefully handled

### Compatibility Issues with Python 3.10+
1. **pylibfreenect2 Dependency**: Needs pylibfreenect2-py310
2. **Import Warnings**: Environment variable checks may fail
3. **OpenCV Compatibility**: May need opencv-python version updates

## Future Enhancements

### Planned Improvements
1. **CUDA Pipeline Support**: Add intelligent pipeline detection
2. **Windows Compatibility**: Test and fix Windows-specific issues
3. **Async Frame Capture**: Non-blocking frame acquisition
4. **Advanced Calibration**: Multi-camera setup support
5. **Real-time Processing**: Built-in filtering and preprocessing

### API Extensions
```python
# Proposed future API
k = ktb.Kinect(auto_pipeline=True)  # Intelligent pipeline selection
stream = k.start_stream()           # Async streaming
filtered_depth = k.get_frame(ktb.DEPTH, filter='median')  # Built-in filtering
```

## Development Environment

### Build and Test Commands
```bash
# Setup development environment
cd kinect-toolbox
pip install -r requirements.txt
pip install -e .

# Run basic test  
python test.py

# Check environment
python -c "import ktb; print('✅ ktb import successful')"
```

### Integration with Parent Project
```bash
# From pylibfreenect2-py310 root:
cd kinect-toolbox
pip install -e .  # Install ktb in development mode

# Test integration
python -c "import ktb; k = ktb.Kinect(); print('✅ Kinect connected')"
```

## Support and Troubleshooting

### Common Issues
1. **"No device connected!"**: Check USB 3.0 connection and drivers
2. **"LIBFREENECT2_INSTALL_PREFIX not set"**: Set environment variable
3. **Pipeline import errors**: Check GPU drivers and SDK installations
4. **Poor performance**: Verify using GPU pipeline, not CPU

### Debug Commands
```python
# Check device detection
import ktb
k = ktb.Kinect()
print(f"Device serial: {k.device.getSerialNumber()}")

# Check pipeline performance
import time
start_time = time.time()
for i in range(30):
    frame = k.get_frame(ktb.COLOR)
fps = 30 / (time.time() - start_time)
print(f"FPS: {fps:.1f}")
```

---

**Project Status**: Functional but needs updates for Python 3.10+ compatibility  
**Main Dependency**: pylibfreenect2-py310 (enhanced version)  
**Target Use Case**: Simplified Kinect v2 development with OpenCV-like API  
**Performance**: 15-35 FPS depending on pipeline selection