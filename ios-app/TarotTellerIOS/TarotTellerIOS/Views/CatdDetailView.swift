import SwiftUI

struct CardDetailView: View {
    let card: TarotCard

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
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

#Preview {
    CardDetailView(card: TarotDeck.sample[0])
}