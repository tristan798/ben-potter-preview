// Cuts Ben out of the studio portrait with Vision, then tightens and feathers the matte.
// usage: cutout <in.png> <out.png> <erodeRadius> <featherRadius>
import Foundation
import Vision
import CoreImage
import CoreImage.CIFilterBuiltins
import AppKit

let a = CommandLine.arguments
let ci = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!
let req = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(ciImage: ci, options: [:])
try handler.perform([req])
let result = req.results!.first!
let maskPB = try result.generateScaledMaskForImage(forInstances: result.allInstances, from: handler)
var mask = CIImage(cvPixelBuffer: maskPB)
let erode = CIFilter.morphologyMinimum(); erode.inputImage = mask; erode.radius = Float(a[3])!
mask = erode.outputImage!
let blur = CIFilter.gaussianBlur(); blur.inputImage = mask; blur.radius = Float(a[4])!
mask = blur.outputImage!.cropped(to: ci.extent)
let gamma = CIFilter.gammaAdjust(); gamma.inputImage = mask; gamma.power = 1.6
mask = gamma.outputImage!
let blend = CIFilter.blendWithMask()
blend.inputImage = ci
blend.backgroundImage = CIImage(color: .clear).cropped(to: ci.extent)
blend.maskImage = mask
let cg = CIContext().createCGImage(blend.outputImage!, from: ci.extent)!
let png = NSBitmapImageRep(cgImage: cg).representation(using: .png, properties: [:])!
try png.write(to: URL(fileURLWithPath: a[2]))
print("ok")
