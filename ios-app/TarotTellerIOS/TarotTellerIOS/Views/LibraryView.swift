import SwiftUI

struct LibraryView: View {
    let cards: [TarotCard]

    var body: some View {
        NavigationStack {
            List(cards) { card in
                NavigationLink(value: card) {
                    VStack(alignment: .leading, spacing: 4) {
                        Text(card.name)
                            .font(.headline)
                        Text(card.keywords.joined(separator: ", "))
                            .font(.caption)
                            .foregroundStyle(.secondary)
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

#Preview {
    LibraryView(cards: TarotDeck.sample)
}