// Transcodes a source video to a web-sized MP4 at an explicit bitrate, and extracts a poster.
// usage: transcode <in> <out.mp4> <poster.jpg> <posterSeconds> <maxHeight> <videoKbps>
import Foundation
import AVFoundation
import AppKit

let a = CommandLine.arguments
let inURL = URL(fileURLWithPath: a[1])
let outURL = URL(fileURLWithPath: a[2])
let posterURL = URL(fileURLWithPath: a[3])
let posterAt = Double(a[4]) ?? 1.0
let maxH = CGFloat(Double(a[5]) ?? 1280)
let kbps = Int(a[6]) ?? 2200

let asset = AVURLAsset(url: inURL)
try? FileManager.default.removeItem(at: outURL)

let vTrack = asset.tracks(withMediaType: .video).first!
let aTrack = asset.tracks(withMediaType: .audio).first
let natural = vTrack.naturalSize.applying(vTrack.preferredTransform)
let srcW = abs(natural.width), srcH = abs(natural.height)
let scale = min(1.0, maxH / srcH)
// keep both dimensions even for H.264
let outW = (Int(srcW * scale) / 2) * 2
let outH = (Int(srcH * scale) / 2) * 2

let reader = try AVAssetReader(asset: asset)
let writer = try AVAssetWriter(outputURL: outURL, fileType: .mp4)
writer.shouldOptimizeForNetworkUse = true   // fast start: moov atom at the front

let vOut = AVAssetReaderTrackOutput(track: vTrack,
    outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
reader.add(vOut)

let vIn = AVAssetWriterInput(mediaType: .video, outputSettings: [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: outW,
    AVVideoHeightKey: outH,
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: kbps * 1000,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        AVVideoMaxKeyFrameIntervalKey: 60,
        AVVideoAllowFrameReorderingKey: true,
    ],
])
vIn.expectsMediaDataInRealTime = false
vIn.transform = vTrack.preferredTransform
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: vIn, sourcePixelBufferAttributes: nil)
writer.add(vIn)

var aOut: AVAssetReaderTrackOutput?
var aIn: AVAssetWriterInput?
if let aTrack = aTrack {
    let o = AVAssetReaderTrackOutput(track: aTrack, outputSettings: [
        AVFormatIDKey: kAudioFormatLinearPCM,
        AVLinearPCMBitDepthKey: 16,
        AVLinearPCMIsFloatKey: false,
        AVLinearPCMIsBigEndianKey: false,
        AVLinearPCMIsNonInterleaved: false,
    ])
    reader.add(o); aOut = o
    let i = AVAssetWriterInput(mediaType: .audio, outputSettings: [
        AVFormatIDKey: kAudioFormatMPEG4AAC,
        AVNumberOfChannelsKey: 2,
        AVSampleRateKey: 44100,
        AVEncoderBitRateKey: 96000,
    ])
    i.expectsMediaDataInRealTime = false
    writer.add(i); aIn = i
}

reader.startReading()
writer.startWriting()
writer.startSession(atSourceTime: .zero)

let group = DispatchGroup()
let vQueue = DispatchQueue(label: "v")
group.enter()
vIn.requestMediaDataWhenReady(on: vQueue) {
    while vIn.isReadyForMoreMediaData {
        if let buf = vOut.copyNextSampleBuffer() {
            vIn.append(buf)
        } else {
            vIn.markAsFinished(); group.leave(); return
        }
    }
}
if let aIn = aIn, let aOut = aOut {
    group.enter()
    aIn.requestMediaDataWhenReady(on: DispatchQueue(label: "a")) {
        while aIn.isReadyForMoreMediaData {
            if let buf = aOut.copyNextSampleBuffer() {
                aIn.append(buf)
            } else {
                aIn.markAsFinished(); group.leave(); return
            }
        }
    }
}
group.wait()
let done = DispatchSemaphore(value: 0)
writer.finishWriting { done.signal() }
done.wait()

if writer.status != .completed {
    print("write failed: \(String(describing: writer.error))"); exit(1)
}

let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true
gen.maximumSize = CGSize(width: 900, height: 1600)
let cg = try gen.copyCGImage(at: CMTime(seconds: posterAt, preferredTimescale: 600), actualTime: nil)
let jpg = NSBitmapImageRep(cgImage: cg).representation(using: .jpeg, properties: [.compressionFactor: 0.78])!
try jpg.write(to: posterURL)
print("ok \(outW)x\(outH)")
