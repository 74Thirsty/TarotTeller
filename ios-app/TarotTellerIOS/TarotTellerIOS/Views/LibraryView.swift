import SwiftUI
import UIKit

struct LibraryView: View {
    let cards: [TarotCard]

    var body: some View {
        NavigationStack {
            List(cards) { card in
                NavigationLink(value: card) {
                    HStack(spacing: 12) {
                        TarotThumbnail(imageName: card.imageName)
                        VStack(alignment: .leading, spacing: 4) {
                        Text(card.name)
                            .font(.headline)
                        Text(card.keywords.joined(separator: ", "))
                            .font(.caption)
                            .foregroundStyle(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("Library")
            .navigationDestination(for: TarotCard.self) { card in
                CardDetailView(card: card)
            }
        }
    }
}

private struct TarotThumbnail: View {
    let imageName: String

    var body: some View {
        if UIImage(named: imageName) != nil {
            Image(imageName)
                .resizable()
                .scaledToFill()
                .frame(width: 44, height: 68)
                .clipped()
                .clipShape(RoundedRectangle(cornerRadius: 8))
        } else {
            RoundedRectangle(cornerRadius: 8)
                .fill(.ultraThinMaterial)
                .frame(width: 44, height: 68)
                .overlay(Image(systemName: "photo"))
        }
    }
}

#Preview {
    LibraryView(cards: TarotDeck.sample)
}

private struct TarotThumbnail: View {
    let imageName: String

    var body: some View {
        if UIImage(named: imageName) != nil {
            Image(imageName)
                .resizable()
                .scaledToFill()
                .frame(width: 44, height: 68)
                .clipped()
                .clipShape(RoundedRectangle(cornerRadius: 8))
        } else {
            RoundedRectangle(cornerRadius: 8)
                .fill(.ultraThinMaterial)
                .frame(width: 44, height: 68)
                .overlay(Image(systemName: "photo"))
        }
    }
}
