import SwiftUI

struct DrawView: View {
    @State private var currentCard = TarotDeck.sample.randomElement()

    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                Text("Daily Draw")
                    .font(.largeTitle.bold())

                if let card = currentCard {
                    VStack(spacing: 12) {
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

#Preview {
    DrawView()
}