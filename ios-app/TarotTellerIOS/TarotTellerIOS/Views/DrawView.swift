import SwiftUI
import UIKit

struct DrawView: View {
    @State private var currentCard = TarotDeck.sample.randomElement()

    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                Text("Daily Draw")
                    .font(.largeTitle.bold())

                if let card = currentCard {
                    VStack(spacing: 12) {
                        TarotCardArtwork(imageName: card.imageName)
                            .frame(height: 220)
                        Text(card.name)
                            .font(.title2.bold())
                        Text(card.keywords.joined(separator: " • "))
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                        Text(card.meaning)
                            .font(.body)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(.thinMaterial)
                    .clipShape(RoundedRectangle(cornerRadius: 20))
                }

                Button(action: drawCard) {
                    Label("Draw another card", systemImage: "shuffle")
                        .font(.headline)
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                .padding(.horizontal)

                Spacer()
            }
            .padding()
            .navigationTitle("TarotTeller")
        }
    }

    private func drawCard() {
        currentCard = TarotDeck.sample.randomElement()
    }
}

private struct TarotCardArtwork: View {
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
                .overlay(Image(systemName: "photo").font(.largeTitle))
        }
    }
}

#Preview {
    DrawView()
}