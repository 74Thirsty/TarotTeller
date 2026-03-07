import SwiftUI
import UIKit

struct CardDetailView: View {
    let cards: [TarotCard]
    let initialCard: TarotCard

    @State private var currentIndex: Int = 0

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                TarotDetailArtwork(imageName: currentCard.imageName)

                HStack(spacing: 12) {
                    Button(action: showPreviousCard) {
                        Label("Previous", systemImage: "chevron.left")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.bordered)
                    .disabled(!hasPreviousCard)

                    Button(action: showNextCard) {
                        Label("Next", systemImage: "chevron.right")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(!hasNextCard)
                }

                Text(currentCard.name)
                    .font(.largeTitle.bold())

                Text(currentCard.arcana.uppercased())
                    .font(.caption)
                    .foregroundStyle(.secondary)

                VStack(alignment: .leading, spacing: 8) {
                    Text("Keywords")
                        .font(.headline)
                    Text(currentCard.keywords.joined(separator: " • "))
                        .font(.body)
                }

                VStack(alignment: .leading, spacing: 8) {
                    Text("Message")
                        .font(.headline)
                    Text(currentCard.meaning)
                        .font(.body)
                        .padding(12)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(.thinMaterial)
                        .clipShape(RoundedRectangle(cornerRadius: 16))
                }
            }
            .padding()
        }
        .navigationTitle(currentCard.name)
        .navigationBarTitleDisplayMode(.inline)
        .onAppear(perform: setInitialIndex)
    }

    private var currentCard: TarotCard {
        cards[currentIndex]
    }

    private var hasPreviousCard: Bool {
        currentIndex > 0
    }

    private var hasNextCard: Bool {
        currentIndex < cards.count - 1
    }

    private func setInitialIndex() {
        guard let index = cards.firstIndex(of: initialCard) else {
            currentIndex = 0
            return
        }
        currentIndex = index
    }

    private func showPreviousCard() {
        guard hasPreviousCard else { return }
        currentIndex -= 1
    }

    private func showNextCard() {
        guard hasNextCard else { return }
        currentIndex += 1
    }
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

#Preview {
    CardDetailView(cards: TarotDeck.sample, initialCard: TarotDeck.sample[0])
}
