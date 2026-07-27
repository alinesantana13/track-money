export function requireText(value, fieldName, maxLength = 255) {
  const trimmedValue = value.trim();
  if (!trimmedValue) {
    throw new Error(`${fieldName} e obrigatorio.`);
  }
  if (trimmedValue.length > maxLength) {
    throw new Error(`${fieldName} deve ter no maximo ${maxLength} caracteres.`);
  }
  return trimmedValue;
}

export function requireEmail(value) {
  const email = value.trim();
  if (!email.includes("@")) {
    throw new Error("Informe um email valido.");
  }
  return email;
}

export function requirePassword(value) {
  if (value.length < 8) {
    throw new Error("A senha deve ter no minimo 8 caracteres.");
  }
  return value;
}

export function requireNonNegativeNumber(value, fieldName) {
  const parsedValue = Number(value);
  if (Number.isNaN(parsedValue) || parsedValue < 0) {
    throw new Error(`${fieldName} deve ser um numero maior ou igual a zero.`);
  }
  return parsedValue;
}
