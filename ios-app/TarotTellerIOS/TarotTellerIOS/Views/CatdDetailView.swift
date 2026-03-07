import SwiftUI
import UIKit

struct CardDetailView: View {
    let card: TarotCard

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                TarotDetailArtwork(imageName: card.imageName)
                Text(card.name)
                    .font(.largeTitle.bold())

                Text(card.arcana.uppercased())
                    .font(.caption)
                    .foregroundStyle(.secondary)

                VStack(alignment: .leading, spacing: 8) {
                    Text("Keywords")
                        .font(.headline)
                    Text(card.keywords.joined(separator: " • "))
                        .font(.body)
                }

                VStack(alignment: .leading, spacing: 8) {
                    Text("Reading")
                        .font(.headline)
                    Text(card.meaning)
                        .font(.body)
                }
            }
            .padding()
        }
        .navigationTitle(card.name)
        .navigationBarTitleDisplayMode(.inline)
    }
}

private struct TarotDetailArtwork: View {
    let imageName: String

    var body: some View {
        if UIImage(named: imageName) != nil {
            Image(imageName)
                .resizable()
                .scaledToFit()
                .clipShape(RoundedRectangle(cornerRadius: 12))
        } else {
            RoundedRectangle(cornerRadius: 12)
                .fill(.ultraThinMaterial)
                .frame(height: 240)
                .overlay(Image(systemName: "photo").font(.largeTitle))
        }
    }
}

#Preview {
    CardDetailView(card: TarotDeck.sample[0])
}

private struct TarotDetailArtwork: View {
    let imageName: String

    var body: some View {
        if UIImage(named: imageName) != nil {
            Image(imageName)
                .resizable()
                .scaledToFit()
                .frame(maxWidth: .infinity, maxHeight: 320)
                .clipShape(RoundedRectangle(cornerRadius: 12))
        } else {
            RoundedRectangle(cornerRadius: 12)
                .fill(.ultraThinMaterial)
                .frame(height: 240)
                .overlay(Image(systemName: "photo").font(.largeTitle))
        }
    }
}
