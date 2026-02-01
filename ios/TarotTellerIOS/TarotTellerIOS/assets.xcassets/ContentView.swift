import SwiftUI

struct TarotCard: Identifiable {
    let id = UUID()
    let name: String
    let upright: String
    let reversed: String
}

struct ContentView: View {
    private let deck: [TarotCard] = [
        TarotCard(
            name: "The Magician",
            upright: "Focus your willpower and act with intention.",
            reversed: "Re-align your tools before moving ahead."
        ),
        TarotCard(
            name: "The High Priestess",
            upright: "Trust the wisdom that lives beneath the surface.",
            reversed: "Invite clarity before committing to a path."
        ),
        TarotCard(
            name: "The Sun",
            upright: "Lean into optimism and shared celebration.",
            reversed: "Let a small ritual restore your confidence."
        )
    ]

    @State private var selectedCard: TarotCard?
    @State private var isReversed = false

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 24) {
                VStack(alignment: .leading, spacing: 8) {
                    Text("TarotTeller")
                        .font(.largeTitle.bold())
                    Text("A gentle daily draw inspired by the Python toolkit.")
                        .font(.title3)
                        .foregroundStyle(.secondary)
                }

                if let selectedCard {
                    VStack(alignment: .leading, spacing: 12) {
                        Text(selectedCard.name)
                            .font(.title2.bold())
                        Text(isReversed ? "Reversed" : "Upright")
                            .font(.caption.weight(.semibold))
                            .foregroundStyle(.secondary)
                        Text(isReversed ? selectedCard.reversed : selectedCard.upright)
                            .font(.body)
                    }
                    .padding()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color(.systemIndigo).opacity(0.1))
                    .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                } else {
                    Text("Tap below to draw your first card.")
                        .foregroundStyle(.secondary)
                }

                Button(action: drawCard) {
                    Label("Draw a Card", systemImage: "sparkles")
                        .font(.headline)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color(.systemIndigo))
                        .foregroundStyle(.white)
                        .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
                }

                Spacer()
            }
            .padding()
            .navigationTitle("Daily Reading")
        }
    }

    private func drawCard() {
        selectedCard = deck.randomElement()
        isReversed = Bool.random()
    }
}

#Preview {
    ContentView()
}