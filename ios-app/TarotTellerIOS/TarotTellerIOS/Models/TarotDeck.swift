import Foundation

enum TarotDeck {
    static let sample: [TarotCard] = [
        TarotCard(
            name: "The Magician",
            arcana: "Major",
            keywords: ["manifestation", "skill", "resourcefulness"],
            meaning: "Channel your focus into one clear intention and let your tools speak."
        ),
        TarotCard(
            name: "The High Priestess",
            arcana: "Major",
            keywords: ["intuition", "mystery", "inner voice"],
            meaning: "Pause before acting; quiet signals reveal the deeper truth."
        ),
        TarotCard(
            name: "The Empress",
            arcana: "Major",
            keywords: ["abundance", "care", "creativity"],
            meaning: "Nurture what you want to grow and let comfort be part of the plan."
        ),
        TarotCard(
            name: "The Emperor",
            arcana: "Major",
            keywords: ["structure", "leadership", "discipline"],
            meaning: "Set the boundary, clarify the rules, and lead with steadiness."
        ),
        TarotCard(
            name: "The Lovers",
            arcana: "Major",
            keywords: ["alignment", "choice", "connection"],
            meaning: "Let your values choose for you and honor the bond you create."
        ),
        TarotCard(
            name: "The Chariot",
            arcana: "Major",
            keywords: ["momentum", "determination", "victory"],
            meaning: "Steer with intention and trust the discipline you have built."
        ),
        TarotCard(
            name: "Strength",
            arcana: "Major",
            keywords: ["courage", "compassion", "resilience"],
            meaning: "Gentle confidence turns struggle into steady progress."
        ),
        TarotCard(
            name: "The Hermit",
            arcana: "Major",
            keywords: ["reflection", "solitude", "wisdom"],
            meaning: "Step back to hear the lesson that only quiet can teach."
        ),
        TarotCard(
            name: "Wheel of Fortune",
            arcana: "Major",
            keywords: ["change", "cycles", "fate"],
            meaning: "Notice the shift and ride the momentum instead of resisting it."
        ),
        TarotCard(
            name: "The Sun",
            arcana: "Major",
            keywords: ["joy", "clarity", "success"],
            meaning: "Lead with optimism; your clarity gives others permission to shine."
        )
    ]
}
