import Foundation
import AVFoundation
let url = URL(fileURLWithPath: CommandLine.arguments[1])
let asset = AVURLAsset(url: url)
let dur = CMTimeGetSeconds(asset.duration)
print("duration: \(String(format: "%.2f", dur))s")
for t in asset.tracks {
    let d = t.naturalSize.applying(t.preferredTransform)
    let w = abs(d.width), h = abs(d.height)
    var codecs: [String] = []
    for desc in t.formatDescriptions {
        let cmd = desc as! CMFormatDescription
        let c = CMFormatDescriptionGetMediaSubType(cmd)
        let bytes = [UInt8((c >> 24) & 0xff), UInt8((c >> 16) & 0xff), UInt8((c >> 8) & 0xff), UInt8(c & 0xff)]
        codecs.append(String(bytes: bytes, encoding: .ascii) ?? "?")
    }
    print("track \(t.mediaType.rawValue): \(Int(w))x\(Int(h)) codec=\(codecs.joined(separator: ",")) bitrate=\(Int(t.estimatedDataRate/1000))kbps fps=\(String(format: "%.1f", t.nominalFrameRate))")
}
